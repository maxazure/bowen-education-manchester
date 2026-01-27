"""
多语言管理路由
"""

import json
from typing import Optional

from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session

from admin.app.database import get_db

router = APIRouter(tags=["i18n"])


# 简化的翻译存储（实际项目中应使用数据库或文件）
TRANSLATIONS = {
    "zh": {
        "site_name": "博文教育",
        "welcome": "欢迎",
        "dashboard": "仪表板",
        "posts": "文章管理",
        "products": "产品管理",
        "galleries": "相册管理",
        "media": "媒体库",
        "settings": "系统设置",
        "logout": "退出登录",
        "save": "保存",
        "cancel": "取消",
        "delete": "删除",
        "edit": "编辑",
        "create": "创建",
        "search": "搜索",
        "loading": "加载中...",
        "no_data": "暂无数据",
        "success": "操作成功",
        "error": "操作失败",
        "confirm_delete": "确定要删除吗？",
        "published": "已发布",
        "draft": "草稿",
        "offline": "已下线",
    },
    "en": {
        "site_name": "Bowen Education",
        "welcome": "Welcome",
        "dashboard": "Dashboard",
        "posts": "Posts",
        "products": "Products",
        "galleries": "Galleries",
        "media": "Media",
        "settings": "Settings",
        "logout": "Logout",
        "save": "Save",
        "cancel": "Cancel",
        "delete": "Delete",
        "edit": "Edit",
        "create": "Create",
        "search": "Search",
        "loading": "Loading...",
        "no_data": "No data",
        "success": "Success",
        "error": "Error",
        "confirm_delete": "Are you sure to delete?",
        "published": "Published",
        "draft": "Draft",
        "offline": "Offline",
    }
}


@router.get("/i18n", response_class=HTMLResponse)
async def i18n_page(
    request: Request,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """多语言管理页面"""
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="admin/templates")

    # 获取所有翻译
    translations = TRANSLATIONS

    # 计算翻译覆盖率
    coverage = {}
    base_keys = set(translations.get("zh", {}).keys())
    for lang, texts in translations.items():
        covered = len(set(texts.keys()) & base_keys)
        total = len(base_keys)
        coverage[lang] = {
            "covered": covered,
            "total": total,
            "percentage": (covered / total * 100) if total > 0 else 0
        }

    return templates.TemplateResponse("i18n.html", {
        "request": request,
        "translations": translations,
        "coverage": coverage,
        "languages": [
            {"code": "zh", "name": "中文", "native_name": "简体中文"},
            {"code": "en", "name": "English", "native_name": "English"},
        ]
    })


@router.get("/api/i18n/{lang}")
async def get_translations(
    lang: str,
    db: Session = Depends(get_db),
):
    """获取指定语言的翻译"""
    if lang not in TRANSLATIONS:
        return JSONResponse(
            content={"success": False, "message": "语言不存在"},
            status_code=404
        )

    return JSONResponse(content={
        "success": True,
        "data": {
            "lang": lang,
            "translations": TRANSLATIONS[lang]
        }
    })


@router.post("/api/i18n/{lang}")
async def update_translations(
    lang: str,
    request: Request,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """更新指定语言的翻译"""
    if lang not in TRANSLATIONS:
        return JSONResponse(
            content={"success": False, "message": "语言不存在"},
            status_code=404
        )

    data = await request.json()
    translations = data.get("translations", {})

    # 更新翻译
    TRANSLATIONS[lang].update(translations)

    return JSONResponse(content={
        "success": True,
        "message": "翻译已更新"
    })


@router.get("/api/i18n")
async def get_all_translations(
    db: Session = Depends(get_db),
):
    """获取所有翻译"""
    return JSONResponse(content={
        "success": True,
        "data": TRANSLATIONS
    })


@router.get("/api/i18n/missing")
async def get_missing_translations(
    source_lang: str = "zh",
    target_lang: str = "en",
    db: Session = Depends(get_db),
):
    """获取缺失的翻译"""
    if source_lang not in TRANSLATIONS or target_lang not in TRANSLATIONS:
        return JSONResponse(
            content={"success": False, "message": "语言不存在"},
            status_code=404
        )

    source_texts = TRANSLATIONS.get(source_lang, {})
    target_texts = TRANSLATIONS.get(target_lang, {})

    missing = {}
    for key, value in source_texts.items():
        if key not in target_texts:
            missing[key] = {
                "source": value,
                "target": "",
                "suggestion": value  # 可以接入翻译API获取建议
            }

    return JSONResponse(content={
        "success": True,
        "data": {
            "source_lang": source_lang,
            "target_lang": target_lang,
            "missing_count": len(missing),
            "missing": missing
        }
    })


@router.post("/api/i18n/export")
async def export_translations(
    request: Request,
    db: Session = Depends(get_db),
):
    """导出翻译文件"""
    from fastapi.responses import StreamingResponse
    import io

    data = await request.json()
    lang = data.get("lang", "zh")
    format = data.get("format", "json")

    if lang not in TRANSLATIONS:
        return JSONResponse(
            content={"success": False, "message": "语言不存在"},
            status_code=404
        )

    if format == "json":
        content = json.dumps(TRANSLATIONS[lang], ensure_ascii=False, indent=2)
        media_type = "application/json"
    elif format == "csv":
        content = "key,original,translation\n"
        for key, value in TRANSLATIONS[lang].items():
            content += f'{key},"{value.replace('"', '""')}",""\n'
        media_type = "text/csv"
    else:
        return JSONResponse(
            content={"success": False, "message": "不支持的格式"},
            status_code=400
        )

    return StreamingResponse(
        iter([content]),
        media_type=media_type,
        headers={
            "Content-Disposition": f"attachment; filename=translations_{lang}.{format}"
        }
    )


@router.post("/api/i18n/import")
async def import_translations(
    request: Request,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """导入翻译文件"""
    from starlette.formparsers import MultiPartBytesStream

    data = await request.form()
    file = data.get("file")
    lang = data.get("lang", "en")

    if not file:
        return JSONResponse(
            content={"success": False, "message": "请选择文件"},
            status_code=400
        )

    try:
        content = await file.read()
        if lang not in TRANSLATIONS:
            TRANSLATIONS[lang] = {}

        # 解析JSON
        translations = json.loads(content)
        TRANSLATIONS[lang].update(translations)

        return JSONResponse(content={
            "success": True,
            "message": f"成功导入 {len(translations)} 条翻译"
        })
    except json.JSONDecodeError:
        return JSONResponse(
            content={"success": False, "message": "无效的JSON格式"},
            status_code=400
        )
    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": f"导入失败: {str(e)}"},
            status_code=500
        )


@router.get("/api/i18n/stats")
async def get_i18n_stats(
    db: Session = Depends(get_db),
):
    """获取翻译统计"""
    stats = {
        "languages": [],
        "total_keys": len(TRANSLATIONS.get("zh", {})),
    }

    for lang, texts in TRANSLATIONS.items():
        total = stats["total_keys"]
        translated = len(texts)
        stats["languages"].append({
            "code": lang,
            "translated": translated,
            "total": total,
            "percentage": (translated / total * 100) if total > 0 else 0
        })

    return JSONResponse(content={
        "success": True,
        "data": stats
    })
