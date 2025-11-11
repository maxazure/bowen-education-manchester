# -*- coding: utf-8 -*-
"""Health Check Routes"""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/health")
async def health_check():
    """健康检查端点"""
    return JSONResponse(
        content={
            "status": "ok",
            "app": "Docms CMS",
            "version": "1.0.0"
        }
    )