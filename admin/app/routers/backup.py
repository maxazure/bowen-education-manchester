"""
数据备份恢复路由
"""

import os
import json
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

router = APIRouter(tags=["backup"])


class BackupResponse(BaseModel):
    success: bool
    message: str
    filename: Optional[str] = None
    size: Optional[int] = None


def get_instance_dir():
    """获取实例目录路径"""
    return Path(__file__).parent.parent.parent.parent / "instance"


def get_backups_dir():
    """获取备份目录路径"""
    backups_dir = get_instance_dir() / "backups"
    if not backups_dir.exists():
        backups_dir.mkdir(parents=True, exist_ok=True)
    return backups_dir


def get_database_path():
    """获取数据库文件路径"""
    return get_instance_dir() / "database.db"


def get_upload_dir():
    """获取上传目录路径"""
    return Path(__file__).parent.parent.parent.parent / "public" / "static" / "uploads"


def backup_database_to_json(db_path: str, output_path: str) -> dict:
    """将SQLite数据库备份为JSON格式"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 获取所有表名
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' AND name NOT LIKE '_alembic_%'")
    tables = [row[0] for row in cursor.fetchall()]

    backup_data = {
        "version": "1.0",
        "created_at": datetime.now().isoformat(),
        "tables": {}
    }

    for table in tables:
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        columns = rows[0].keys() if rows else []

        backup_data["tables"][table] = {
            "columns": list(columns),
            "rows": [dict(row) for row in rows]
        }

    conn.close()

    # 写入JSON文件
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(backup_data, f, ensure_ascii=False, indent=2)

    return backup_data


def restore_database_from_json(json_path: str, db_path: str) -> dict:
    """从JSON备份恢复数据库"""
    with open(json_path, 'r', encoding='utf-8') as f:
        backup_data = json.load(f)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    restored_count = 0

    for table_name, table_data in backup_data.get("tables", {}).items():
        # 清空现有数据
        cursor.execute(f"DELETE FROM {table_name}")

        if table_data["rows"]:
            columns = table_data["columns"]
            placeholders = ",".join(["?" for _ in columns])
            insert_sql = f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({placeholders})"

            for row in table_data["rows"]:
                values = [row.get(col) for col in columns]
                cursor.execute(insert_sql, values)
                restored_count += 1

    conn.commit()
    conn.close()

    return {"restored_count": restored_count}


@router.get("/backup", response_class=JSONResponse)
async def backup_page(request: Request):
    """备份管理页面"""
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="admin/templates")

    backups_dir = get_backups_dir()
    database_path = get_database_path()

    # 获取备份列表
    backups = []
    if backups_dir.exists():
        for f in sorted(backups_dir.glob("*.json"), reverse=True):
            stat = f.stat()
            backups.append({
                "filename": f.name,
                "size": stat.st_size,
                "size_formatted": f"{stat.st_size / 1024:.1f} KB",
                "created_at": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                "url": f"/admin/api/backup/download?filename={f.name}"
            })

    return templates.TemplateResponse("backup.html", {
        "request": request,
        "backups": backups,
        "database_size": database_path.stat().st_size if database_path.exists() else 0,
    })


@router.post("/api/backup/create")
async def create_backup() -> BackupResponse:
    """创建数据库备份"""
    try:
        db_path = str(get_database_path())
        backups_dir = get_backups_dir()

        if not Path(db_path).exists():
            raise HTTPException(status_code=404, detail="数据库文件不存在")

        # 生成备份文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"backup_{timestamp}.json"
        output_path = backups_dir / filename

        # 执行备份
        backup_database_to_json(db_path, str(output_path))

        return BackupResponse(
            success=True,
            message="备份创建成功",
            filename=filename,
            size=output_path.stat().st_size
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"备份失败: {str(e)}")


@router.get("/api/backup/download")
async def download_backup(filename: str):
    """下载备份文件"""
    backups_dir = get_backups_dir()
    file_path = backups_dir / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="备份文件不存在")

    return FileResponse(
        path=str(file_path),
        filename=filename,
        media_type="application/json"
    )


@router.delete("/api/backup/{filename}")
async def delete_backup(filename: str) -> BackupResponse:
    """删除备份文件"""
    try:
        backups_dir = get_backups_dir()
        file_path = backups_dir / filename

        if not file_path.exists():
            raise HTTPException(status_code=404, detail="备份文件不存在")

        file_path.unlink()

        return BackupResponse(
            success=True,
            message="备份已删除"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除失败: {str(e)}")


@router.post("/api/backup/restore")
async def restore_backup(request: Request) -> BackupResponse:
    """恢复数据库备份"""
    try:
        from starlette.formparsers import MultiPartBytesStream

        # 获取上传的备份文件
        form = await request.form()
        file = form.get("file")

        if not file:
            raise HTTPException(status_code=400, detail="请选择备份文件")

        # 验证文件类型
        if not file.filename.endswith(".json"):
            raise HTTPException(status_code=400, detail="仅支持 .json 格式的备份文件")

        # 保存上传的文件到临时目录
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix=".json", delete=False, encoding='utf-8') as tmp:
            content = await file.read()
            # 尝试解析JSON验证文件格式
            json.loads(content)
            tmp.write(content)
            tmp_path = tmp.name

        try:
            # 执行恢复
            db_path = str(get_database_path())
            result = restore_database_from_json(tmp_path, db_path)

            return BackupResponse(
                success=True,
                message=f"恢复成功，共恢复 {result['restored_count']} 条记录"
            )
        finally:
            # 清理临时文件
            Path(tmp_path).unlink(missing_ok=True)

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="无效的JSON格式")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"恢复失败: {str(e)}")


@router.get("/api/backup/stats")
async def backup_stats() -> dict:
    """获取备份统计信息"""
    try:
        backups_dir = get_backups_dir()
        database_path = get_database_path()

        # 数据库信息
        db_size = database_path.stat().st_size if database_path.exists() else 0

        # 备份列表
        backups = []
        if backups_dir.exists():
            for f in sorted(backups_dir.glob("*.json"), reverse=True):
                backups.append({
                    "name": f.name,
                    "size": f.stat().st_size
                })

        total_backup_size = sum(b["size"] for b in backups)

        return {
            "success": True,
            "data": {
                "database_size": db_size,
                "database_size_formatted": f"{db_size / 1024 / 1024:.2f} MB",
                "backup_count": len(backups),
                "total_backup_size": total_backup_size,
                "total_backup_size_formatted": f"{total_backup_size / 1024:.1f} KB"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取统计信息失败: {str(e)}")
