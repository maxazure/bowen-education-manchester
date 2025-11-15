from typing import Optional
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from admin.app.database import get_db
from admin.app.services import layout_service
from app.models.layout import LayoutScope


router = APIRouter(prefix="/home", tags=["home"])
templates = Jinja2Templates(directory="admin/templates")


@router.get("", response_class=HTMLResponse)
async def home_manager(request: Request, db: Session = Depends(get_db)):
    draft = layout_service.get_or_create_draft(db, LayoutScope.HOME)
    tree = layout_service.read_layout_tree(db, draft)
    return templates.TemplateResponse("home/manager.html", {"request": request, "tree": tree})


@router.get("/data")
async def read_home_data(db: Session = Depends(get_db)):
    draft = layout_service.get_or_create_draft(db, LayoutScope.HOME)
    return layout_service.read_layout_tree(db, draft)


@router.post("/sections")
async def upsert_home_section(
    layout_id: int,
    section_id: Optional[int] = None,
    title: Optional[str] = None,
    sort_order: Optional[int] = None,
    is_enabled: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    s = layout_service.upsert_section(db, layout_id, section_id, title, sort_order, is_enabled)
    return {"id": s.id}


@router.post("/sections/reorder")
async def reorder_home_sections(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    layout_id = data.get("layout_id")
    count = layout_service.reorder_sections(db, layout_id, data.get("order", []))
    return {"updated": count}


@router.post("/blocks")
async def upsert_home_block(
    section_id: int,
    block_id: Optional[int] = None,
    block_type: str = "RichText",
    attributes_json: Optional[str] = None,
    sort_order: Optional[int] = None,
    is_enabled: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    b = layout_service.upsert_block(db, section_id, block_id, block_type, attributes_json, sort_order, is_enabled)
    return {"id": b.id}


@router.put("/blocks/{block_id}")
async def update_home_block(
    block_id: int,
    attributes_json: str,
    db: Session = Depends(get_db),
):
    from app.models.layout import PageLayoutBlock
    b = db.query(PageLayoutBlock).filter_by(id=block_id).first()
    if not b:
        return JSONResponse(status_code=404, content={"error": "Block not found"})
    b.attributes_json = attributes_json
    db.commit()
    return {"id": b.id}


@router.post("/blocks/reorder")
async def reorder_home_blocks(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    section_id = data.get("section_id")
    count = layout_service.reorder_blocks(db, section_id, data.get("order", []))
    return {"updated": count}


@router.delete("/blocks/{block_id}")
async def delete_home_block(block_id: int, db: Session = Depends(get_db)):
    from app.models.layout import PageLayoutBlock
    b = db.query(PageLayoutBlock).filter_by(id=block_id).first()
    if not b:
        return JSONResponse(status_code=404, content={"error": "Block not found"})
    db.delete(b)
    db.commit()
    return {"deleted": block_id}


@router.post("/publish")
async def publish_home(db: Session = Depends(get_db)):
    draft = layout_service.get_or_create_draft(db, LayoutScope.HOME)
    layout = layout_service.publish_layout(db, draft.id)
    return {"status": layout.status, "published_at": layout.published_at.isoformat() if layout.published_at else None}


@router.get("/preview", response_class=HTMLResponse)
async def preview_home(request: Request, db: Session = Depends(get_db)):
    draft = layout_service.get_or_create_draft(db, LayoutScope.HOME)
    html = layout_service.render_layout_html(db, draft)
    return templates.TemplateResponse("home/preview.html", {"request": request, "html": html})