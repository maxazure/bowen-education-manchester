"""
管理后台工具函数
"""

from datetime import datetime
from typing import Any, Dict


def format_datetime(dt: datetime, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    格式化日期时间

    Args:
        dt: 日期时间对象
        fmt: 格式字符串

    Returns:
        格式化后的字符串
    """
    if dt is None:
        return ""
    return dt.strftime(fmt)


def success_response(data: Any = None, message: str = "操作成功") -> Dict:
    """
    成功响应格式

    Args:
        data: 响应数据
        message: 提示信息

    Returns:
        标准响应字典
    """
    return {"success": True, "message": message, "data": data}


def error_response(message: str = "操作失败", code: int = 400) -> Dict:
    """
    错误响应格式

    Args:
        message: 错误信息
        code: 错误代码

    Returns:
        标准响应字典
    """
    return {"success": False, "message": message, "code": code}
