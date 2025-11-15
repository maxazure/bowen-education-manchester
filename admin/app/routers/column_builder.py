from typing import Optional
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from admin.app.database import get_db
from admin.app.services import layout_service
from app.models.layout import LayoutScope


router = APIRouter(prefix="/columns", tags=["columns-builder"])
templates = Jinja2Templates(directory="admin/templates")


@router.get("/{column_id}/builder", response_class=HTMLResponse)
async def column_builder(request: Request, column_id: int, db: Session = Depends(get_db)):
    draft = layout_service.get_or_create_draft(db, LayoutScope.COLUMN, scope_id=column_id)
    tree = layout_service.read_layout_tree(db, draft)
    return templates.TemplateResponse("home/manager.html", {"request": request, "tree": tree, "column_id": column_id})


@router.get("/{column_id}/builder/data")
async def read_column_builder_data(column_id: int, db: Session = Depends(get_db)):
    draft = layout_service.get_or_create_draft(db, LayoutScope.COLUMN, scope_id=column_id)
    return layout_service.read_layout_tree(db, draft)


@router.post("/{column_id}/builder/sections")
async def upsert_column_section(
    column_id: int,
    layout_id: int,
    section_id: Optional[int] = None,
    title: Optional[str] = None,
    sort_order: Optional[int] = None,
    is_enabled: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    s = layout_service.upsert_section(db, layout_id, section_id, title, sort_order, is_enabled)
    return {"id": s.id}


@router.post("/{column_id}/builder/sections/reorder")
async def reorder_column_sections(column_id: int, request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    layout_id = data.get("layout_id")
    count = layout_service.reorder_sections(db, layout_id, data.get("order", []))
    return {"updated": count}


@router.post("/{column_id}/builder/blocks")
async def upsert_column_block(
    column_id: int,
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


@router.put("/{column_id}/builder/blocks/{block_id}")
async def update_column_block(
    column_id: int,
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


@router.post("/{column_id}/builder/blocks/reorder")
async def reorder_column_blocks(column_id: int, request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    section_id = data.get("section_id")
    count = layout_service.reorder_blocks(db, section_id, data.get("order", []))
    return {"updated": count}


@router.delete("/{column_id}/builder/blocks/{block_id}")
async def delete_column_block(column_id: int, block_id: int, db: Session = Depends(get_db)):
    from app.models.layout import PageLayoutBlock
    b = db.query(PageLayoutBlock).filter_by(id=block_id).first()
    if not b:
        return JSONResponse(status_code=404, content={"error": "Block not found"})
    db.delete(b)
    db.commit()
    return {"deleted": block_id}


@router.post("/{column_id}/builder/publish")
async def publish_column_layout(column_id: int, db: Session = Depends(get_db)):
    draft = layout_service.get_or_create_draft(db, LayoutScope.COLUMN, scope_id=column_id)
    layout = layout_service.publish_layout(db, draft.id)
    return {"status": layout.status}


@router.get("/{column_id}/builder/preview", response_class=HTMLResponse)
async def preview_column_layout(request: Request, column_id: int, db: Session = Depends(get_db)):
    draft = layout_service.get_or_create_draft(db, LayoutScope.COLUMN, scope_id=column_id)
    html = layout_service.render_layout_html(db, draft)
    return templates.TemplateResponse("home/preview.html", {"request": request, "html": html, "column_id": column_id})