"""
Hero幻灯片管理路由

提供Hero幻灯片的 CRUD 操作、排序等功能
"""

from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from admin.app.database import get_db
from app.models.hero import HeroSlide

# 获取admin目录的绝对路径
ADMIN_DIR = Path(__file__).parent.parent.parent
templates = Jinja2Templates(directory=str(ADMIN_DIR / "templates"))

router = APIRouter(prefix="/heroes", tags=["heroes"])


# ===== HTML 页面路由 =====


@router.get("", response_class=HTMLResponse)
async def list_heroes(
    request: Request,
    db: Session = Depends(get_db),
):
    """Hero幻灯片列表页面"""
    # 获取所有Hero幻灯片，按排序顺序排列
    heroes = db.query(HeroSlide).order_by(HeroSlide.sort_order.asc(), HeroSlide.created_at.desc()).all()

    # 计算统计信息
    total_heroes = len(heroes)
    active_heroes = len([h for h in heroes if h.is_active])
    inactive_heroes = len([h for h in heroes if not h.is_active])

    return templates.TemplateResponse(
        "heroes/list.html",
        {
            "request": request,
            "heroes": heroes,
            "total_heroes": total_heroes,
            "active_heroes": active_heroes,
            "inactive_heroes": inactive_heroes,
        }
    )


@router.get("/new", response_class=HTMLResponse)
async def new_hero(request: Request):
    """新建Hero幻灯片页面"""
    return templates.TemplateResponse(
        "heroes/form.html",
        {
            "request": request,
            "hero": None,
            "is_edit": False,
        }
    )


@router.get("/{hero_id}/edit", response_class=HTMLResponse)
async def edit_hero(
    request: Request,
    hero_id: int,
    db: Session = Depends(get_db),
):
    """编辑Hero幻灯片页面"""
    hero = db.query(HeroSlide).filter(HeroSlide.id == hero_id).first()
    if not hero:
        raise HTTPException(status_code=404, detail="Hero幻灯片不存在")

    return templates.TemplateResponse(
        "heroes/form.html",
        {
            "request": request,
            "hero": hero,
            "is_edit": True,
        }
    )


# ===== API 路由 =====


@router.post("", response_class=HTMLResponse)
async def create_hero(
    request: Request,
    db: Session = Depends(get_db),
    title: str = Form(...),
    title_en: Optional[str] = Form(None),
    subtitle: Optional[str] = Form(None),
    subtitle_en: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    description_en: Optional[str] = Form(None),
    background_image: str = Form(...),
    badge_text: Optional[str] = Form(None),
    badge_text_en: Optional[str] = Form(None),
    button_text: Optional[str] = Form(None),
    button_text_en: Optional[str] = Form(None),
    button_url: Optional[str] = Form(None),
    button_style: Optional[str] = Form("btn-primary"),
    button2_text: Optional[str] = Form(None),
    button2_text_en: Optional[str] = Form(None),
    button2_url: Optional[str] = Form(None),
    button2_style: Optional[str] = Form("btn-outline-light"),
    sort_order: int = Form(0),
    is_active: bool = Form(True),
):
    """创建新的Hero幻灯片"""
    hero = HeroSlide(
        title=title,
        title_en=title_en if title_en else None,
        subtitle=subtitle if subtitle else None,
        subtitle_en=subtitle_en if subtitle_en else None,
        description=description if description else None,
        description_en=description_en if description_en else None,
        background_image=background_image,
        badge_text=badge_text if badge_text else None,
        badge_text_en=badge_text_en if badge_text_en else None,
        button_text=button_text if button_text else None,
        button_text_en=button_text_en if button_text_en else None,
        button_url=button_url if button_url else None,
        button_style=button_style,
        button2_text=button2_text if button2_text else None,
        button2_text_en=button2_text_en if button2_text_en else None,
        button2_url=button2_url if button2_url else None,
        button2_style=button2_style,
        sort_order=sort_order,
        is_active=is_active,
    )

    db.add(hero)
    db.commit()
    db.refresh(hero)

    return RedirectResponse(url="/admin/heroes", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/{hero_id}", response_class=HTMLResponse)
async def update_hero(
    request: Request,
    hero_id: int,
    db: Session = Depends(get_db),
    title: str = Form(...),
    title_en: Optional[str] = Form(None),
    subtitle: Optional[str] = Form(None),
    subtitle_en: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    description_en: Optional[str] = Form(None),
    background_image: str = Form(...),
    badge_text: Optional[str] = Form(None),
    badge_text_en: Optional[str] = Form(None),
    button_text: Optional[str] = Form(None),
    button_text_en: Optional[str] = Form(None),
    button_url: Optional[str] = Form(None),
    button_style: Optional[str] = Form("btn-primary"),
    button2_text: Optional[str] = Form(None),
    button2_text_en: Optional[str] = Form(None),
    button2_url: Optional[str] = Form(None),
    button2_style: Optional[str] = Form("btn-outline-light"),
    sort_order: int = Form(0),
    is_active: bool = Form(True),
):
    """更新Hero幻灯片"""
    hero = db.query(HeroSlide).filter(HeroSlide.id == hero_id).first()
    if not hero:
        raise HTTPException(status_code=404, detail="Hero幻灯片不存在")

    hero.title = title
    hero.title_en = title_en if title_en else None
    hero.subtitle = subtitle if subtitle else None
    hero.subtitle_en = subtitle_en if subtitle_en else None
    hero.description = description if description else None
    hero.description_en = description_en if description_en else None
    hero.background_image = background_image
    hero.badge_text = badge_text if badge_text else None
    hero.badge_text_en = badge_text_en if badge_text_en else None
    hero.button_text = button_text if button_text else None
    hero.button_text_en = button_text_en if button_text_en else None
    hero.button_url = button_url if button_url else None
    hero.button_style = button_style
    hero.button2_text = button2_text if button2_text else None
    hero.button2_text_en = button2_text_en if button2_text_en else None
    hero.button2_url = button2_url if button2_url else None
    hero.button2_style = button2_style
    hero.sort_order = sort_order
    hero.is_active = is_active

    db.commit()

    return RedirectResponse(url="/admin/heroes", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/{hero_id}/delete")
async def delete_hero(
    hero_id: int,
    db: Session = Depends(get_db),
):
    """删除Hero幻灯片"""
    hero = db.query(HeroSlide).filter(HeroSlide.id == hero_id).first()
    if not hero:
        raise HTTPException(status_code=404, detail="Hero幻灯片不存在")

    db.delete(hero)
    db.commit()

    return RedirectResponse(url="/admin/heroes", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/{hero_id}/toggle-status")
async def toggle_hero_status(
    hero_id: int,
    db: Session = Depends(get_db),
):
    """切换Hero幻灯片的启用状态"""
    hero = db.query(HeroSlide).filter(HeroSlide.id == hero_id).first()
    if not hero:
        raise HTTPException(status_code=404, detail="Hero幻灯片不存在")

    hero.is_active = not hero.is_active
    db.commit()

    return RedirectResponse(url="/admin/heroes", status_code=status.HTTP_303_SEE_OTHER)
