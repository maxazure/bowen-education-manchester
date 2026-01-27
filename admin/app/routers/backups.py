"""
备份管理路由
"""

import os
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session

from admin.app.database import get_db

router = APIRouter(tags=["backups"])

# 备份目录
BACKUP_DIR = Path("instance/backups")
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

# 保留天数
RETENTION_DAYS = 7


def get_backup_files():
    """获取所有备份文件"""
    backups = []
    if not BACKUP_DIR.exists():
        return backups

    for f in BACKUP_DIR.iterdir():
        if f.is_file() and f.suffix == '.zip':
            stat = f.stat()
            mtime = datetime.fromtimestamp(stat.st_mtime)
            size = stat.st_size

            # 解析文件名
            name = f.stem  # without extension
            parts = name.split('_')
            if len(parts) >= 3:
                timestamp = parts[0]
                backup_type = parts[1] if len(parts) > 1 else 'full'
                label = '_'.join(parts[2:]) if len(parts) > 2 else ''

                backups.append({
                    'name': f.name,
                    'timestamp': timestamp,
                    'type': backup_type,
                    'label': label,
                    'size': format_size(size),
                    'time': mtime.strftime('%Y-%m-%d %H:%M'),
                    'mtime': mtime,
                    'download': f'/admin/api/backups/download/{f.name}'
                })

    # 按时间排序
    backups.sort(key=lambda x: x['mtime'], reverse=True)
    return backups


def format_size(size):
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


@router.get("/api/backups")
async def list_backups():
    """获取备份列表"""
    backups = get_backup_files()
    return JSONResponse(content={
        "success": True,
        "data": backups
    })


@router.post("/api/backups/create")
async def create_backup(
    include_database: bool = True,
    include_uploads: bool = False,
    label: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """创建备份"""
    import zipfile

    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_types = []

        if include_database:
            backup_types.append('db')
        if include_uploads:
            backup_types.append('uploads')

        backup_type = '+'.join(backup_types) if len(backup_types) > 1 else backup_types[0]

        label_suffix = f"_{label}" if label else ""
        filename = f"{timestamp}_{backup_type}{label_suffix}.zip"
        backup_path = BACKUP_DIR / filename

        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            # 备份数据库
            if include_database:
                db_path = Path("instance/database.db")
                if db_path.exists():
                    zf.write(db_path, "database.db")

                # 备份迁移记录
                migrations_dir = Path("migrations/versions")
                if migrations_dir.exists():
                    for f in migrations_dir.iterdir():
                        if f.is_file() and f.suffix == '.py':
                            zf.write(f, f"migrations/{f.name}")

            # 备份上传文件
            if include_uploads:
                uploads_dir = Path("public/static/uploads")
                if uploads_dir.exists():
                    for root, dirs, files in os.walk(uploads_dir):
                        for file in files:
                            file_path = Path(root) / file
                            arcname = file_path.relative_to(Path("public"))
                            zf.write(file_path, arcname)

        return JSONResponse(content={
            "success": True,
            "message": f"备份创建成功: {filename}",
            "data": {
                "filename": filename,
                "size": format_size(backup_path.stat().st_size)
            }
        }, status_code=status.HTTP_201_CREATED)

    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": f"备份失败: {str(e)}"},
            status_code=status.HTTP_400_BAD_REQUEST
        )


@router.get("/api/backups/download/{filename}")
async def download_backup(filename: str):
    """下载备份文件"""
    backup_path = BACKUP_DIR / filename

    if not backup_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="备份文件不存在"
        )

    return FileResponse(
        path=str(backup_path),
        filename=filename,
        media_type='application/zip'
    )


@router.delete("/api/backups/{filename}")
async def delete_backup(filename: str):
    """删除备份"""
    backup_path = BACKUP_DIR / filename

    if not backup_path.exists():
        return JSONResponse(
            content={"success": False, "message": "备份文件不存在"},
            status_code=status.HTTP_404_NOT_FOUND
        )

    try:
        backup_path.unlink()
        return JSONResponse(content={
            "success": True,
            "message": "备份已删除"
        })

    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": f"删除失败: {str(e)}"},
            status_code=status.HTTP_400_BAD_REQUEST
        )


@router.post("/api/backups/clear-old")
async def clear_old_backups():
    """清理旧备份"""
    try:
        cutoff_date = datetime.now()
        deleted = 0

        for f in BACKUP_DIR.iterdir():
            if f.is_file() and f.suffix == '.zip':
                mtime = datetime.fromtimestamp(f.stat().st_mtime)
                age = (cutoff_date - mtime).days

                if age > RETENTION_DAYS:
                    f.unlink()
                    deleted += 1

        return JSONResponse(content={
            "success": True,
            "message": f"已删除 {deleted} 个旧备份"
        })

    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": f"清理失败: {str(e)}"},
            status_code=status.HTTP_400_BAD_REQUEST
        )
