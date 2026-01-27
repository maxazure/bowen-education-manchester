"""
评论管理路由
"""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Form, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session

from admin.app.database import get_db
from app.models import Comment, Post

router = APIRouter(tags=["comments"])
templates = None  # 将在需要时动态导入


@router.get("/comments", response_class=HTMLResponse)
async def comments_list(
    request: Request,
    db: Session = Depends(get_db),
    status: Optional[str] = None,
    content_type: Optional[str] = None,
    keyword: Optional[str] = None,
    page: int = 1,
):
    """评论列表页面"""
    global templates
    if templates is None:
        from fastapi.templating import Jinja2Templates
        templates = Jinja2Templates(directory="admin/templates")

    query = db.query(Comment)

    if status:
        query = query.filter(Comment.status == status)
    if content_type:
        query = query.filter(Comment.content_type == content_type)
    if keyword:
        query = query.filter(
            (Comment.author_name.contains(keyword)) |
            (Comment.content.contains(keyword))
        )

    # 统计
    total = query.count()
    pending = db.query(Comment).filter(Comment.status == "pending").count()
    approved = db.query(Comment).filter(Comment.status == "approved").count()
    rejected = db.query(Comment).filter(Comment.status == "rejected").count()

    # 分页
    per_page = 20
    comments = query.order_by(Comment.created_at.desc()).offset((page - 1) * per_page).limit(per_page).all()

    return templates.TemplateResponse("comments/list.html", {
        "request": request,
        "comments": comments,
        "total": total,
        "pending": pending,
        "approved": approved,
        "rejected": rejected,
        "current_status": status,
        "current_type": content_type,
        "current_keyword": keyword,
        "page": page,
        "per_page": per_page,
    })


@router.get("/api/comments")
async def get_comments_api(
    db: Session = Depends(get_db),
    status: Optional[str] = None,
    content_type: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """获取评论列表 API"""
    query = db.query(Comment)

    if status:
        query = query.filter(Comment.status == status)
    if content_type:
        query = query.filter(Comment.content_type == content_type)

    total = query.count()
    comments = query.order_by(Comment.created_at.desc()).offset(offset).limit(limit).all()

    return JSONResponse(content={
        "success": True,
        "data": [c.to_dict() for c in comments],
        "total": total,
    })


@router.post("/comments/{comment_id}/approve")
async def approve_comment(
    comment_id: int,
    db: Session = Depends(get_db),
):
    """审核通过评论"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        return JSONResponse(content={"success": False, "message": "评论不存在"}, status_code=404)

    comment.status = "approved"
    comment.reviewed_at = datetime.now()
    db.commit()

    return JSONResponse(content={"success": True, "message": "已通过审核"})


@router.post("/comments/{comment_id}/reject")
async def reject_comment(
    comment_id: int,
    db: Session = Depends(get_db),
):
    """审核拒绝评论"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        return JSONResponse(content={"success": False, "message": "评论不存在"}, status_code=404)

    comment.status = "rejected"
    comment.reviewed_at = datetime.now()
    db.commit()

    return JSONResponse(content={"success": True, "message": "已拒绝"})


@router.post("/comments/{comment_id}/spam")
async def mark_spam(
    comment_id: int,
    db: Session = Depends(get_db),
):
    """标记为垃圾评论"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        return JSONResponse(content={"success": False, "message": "评论不存在"}, status_code=404)

    comment.status = "spam"
    comment.reviewed_at = datetime.now()
    db.commit()

    return JSONResponse(content={"success": True, "message": "已标记为垃圾评论"})


@router.post("/comments/{comment_id}/reply")
async def reply_comment(
    comment_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    """回复评论"""
    data = await request.json()
    reply_content = data.get("content", "").strip()

    if not reply_content:
        return JSONResponse(content={"success": False, "message": "回复内容不能为空"}, status_code=400)

    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        return JSONResponse(content={"success": False, "message": "评论不存在"}, status_code=404)

    comment.reply_content = reply_content
    comment.status = "approved"
    comment.reviewed_at = datetime.now()
    db.commit()

    return JSONResponse(content={"success": True, "message": "回复成功"})


@router.post("/comments/{comment_id}/delete")
async def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
):
    """删除评论"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        return JSONResponse(content={"success": False, "message": "评论不存在"}, status_code=404)

    db.delete(comment)
    db.commit()

    return JSONResponse(content={"success": True, "message": "已删除"})


@router.post("/comments/batch-action")
async def batch_action(
    request: Request,
    db: Session = Depends(get_db),
):
    """批量操作"""
    data = await request.json()
    comment_ids = data.get("comment_ids", [])
    action = data.get("action", "")

    if not comment_ids or not action:
        return JSONResponse(content={"success": False, "message": "参数错误"}, status_code=400)

    comments = db.query(Comment).filter(Comment.id.in_(comment_ids)).all()

    if action == "approve":
        for c in comments:
            c.status = "approved"
            c.reviewed_at = datetime.now()
        message = f"已通过审核 {len(comments)} 条评论"
    elif action == "reject":
        for c in comments:
            c.status = "rejected"
            c.reviewed_at = datetime.now()
        message = f"已拒绝 {len(comments)} 条评论"
    elif action == "spam":
        for c in comments:
            c.status = "spam"
            c.reviewed_at = datetime.now()
        message = f"已标记 {len(comments)} 条为垃圾评论"
    elif action == "delete":
        for c in comments:
            db.delete(c)
        message = f"已删除 {len(comments)} 条评论"
    else:
        return JSONResponse(content={"success": False, "message": "无效操作"}, status_code=400)

    db.commit()

    return JSONResponse(content={"success": True, "message": message})


@router.get("/comments/stats")
async def get_comments_stats(
    db: Session = Depends(get_db),
):
    """获取评论统计"""
    total = db.query(Comment).count()
    pending = db.query(Comment).filter(Comment.status == "pending").count()
    approved = db.query(Comment).filter(Comment.status == "approved").count()
    rejected = db.query(Comment).filter(Comment.status == "rejected").count()
    spam = db.query(Comment).filter(Comment.status == "spam").count()

    return JSONResponse(content={
        "success": True,
        "data": {
            "total": total,
            "pending": pending,
            "approved": approved,
            "rejected": rejected,
            "spam": spam,
        }
    })
