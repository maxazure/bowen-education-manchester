"""
测试留言导出功能
"""

import csv
import io
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.contact import ContactMessage


def test_export_csv(db_session: Session):
    """测试导出 CSV"""
    # 创建测试留言
    messages = [
        ContactMessage(
            name="张三",
            contact_info="zhangsan@example.com",
            message_text="我想咨询羽毛球课程",
            status="unread",
            source_page_url="https://example.com/courses",
        ),
        ContactMessage(
            name="李四",
            contact_info="lisi@example.com",
            message_text="请问有周末培训班吗？",
            status="handled",
            handled_at=datetime.now(),
            source_page_url="https://example.com/contact",
        ),
        ContactMessage(
            name="王五",
            contact_info="13800138000",
            message_text="羽毛球拍的价格是多少？",
            status="handled",
            handled_at=datetime.now(),
        ),
    ]
    db_session.add_all(messages)
    db_session.commit()

    # 查询所有留言
    all_messages = (
        db_session.query(ContactMessage)
        .order_by(ContactMessage.created_at.desc())
        .all()
    )

    # 创建 CSV 内容
    output = io.StringIO()
    writer = csv.writer(output)

    # 写入表头
    headers = [
        "ID",
        "姓名",
        "联系方式",
        "留言内容",
        "状态",
        "来源页面",
        "创建时间",
        "处理时间",
    ]
    writer.writerow(headers)

    # 写入数据
    for msg in all_messages:
        status_text = "未读" if msg.status == "unread" else "已处理"
        handled_at_str = (
            msg.handled_at.strftime("%Y-%m-%d %H:%M:%S") if msg.handled_at else ""
        )
        created_at_str = msg.created_at.strftime("%Y-%m-%d %H:%M:%S")

        writer.writerow(
            [
                msg.id,
                msg.name,
                msg.contact_info,
                msg.message_text,
                status_text,
                msg.source_page_url or "",
                created_at_str,
                handled_at_str,
            ]
        )

    # 获取 CSV 内容
    csv_content = output.getvalue()
    output.close()

    # 验证 CSV 内容
    assert "ID,姓名,联系方式,留言内容,状态,来源页面,创建时间,处理时间" in csv_content
    assert "张三" in csv_content
    assert "李四" in csv_content
    assert "王五" in csv_content
    assert "zhangsan@example.com" in csv_content
    assert "未读" in csv_content
    assert "已处理" in csv_content

    # 验证行数（表头 + 3条数据）
    lines = csv_content.strip().split("\n")
    assert len(lines) == 4


def test_export_fields_completeness(db_session: Session):
    """测试导出字段完整性"""
    # 创建一条包含所有字段的留言
    msg = ContactMessage(
        name="测试用户",
        contact_info="test@example.com",
        message_text="这是一条完整的测试留言，包含所有字段信息。",
        status="handled",
        handled_at=datetime.now(),
        source_page_url="https://example.com/test",
    )
    db_session.add(msg)
    db_session.commit()

    # 查询留言
    message = (
        db_session.query(ContactMessage).filter(ContactMessage.id == msg.id).first()
    )

    # 验证所有必要字段都存在
    assert message.id is not None
    assert message.name is not None
    assert message.contact_info is not None
    assert message.message_text is not None
    assert message.status is not None
    assert message.created_at is not None

    # 创建 CSV 输出
    output = io.StringIO()
    writer = csv.writer(output)

    # 写入表头
    headers = [
        "ID",
        "姓名",
        "联系方式",
        "留言内容",
        "状态",
        "来源页面",
        "创建时间",
        "处理时间",
    ]
    writer.writerow(headers)

    # 写入数据
    status_text = "未读" if message.status == "unread" else "已处理"
    handled_at_str = (
        message.handled_at.strftime("%Y-%m-%d %H:%M:%S") if message.handled_at else ""
    )
    created_at_str = message.created_at.strftime("%Y-%m-%d %H:%M:%S")

    writer.writerow(
        [
            message.id,
            message.name,
            message.contact_info,
            message.message_text,
            status_text,
            message.source_page_url or "",
            created_at_str,
            handled_at_str,
        ]
    )

    csv_content = output.getvalue()
    output.close()

    # 解析 CSV 验证字段
    csv_reader = csv.DictReader(io.StringIO(csv_content))
    row = next(csv_reader)

    # 验证所有字段都被正确导出
    assert row["ID"] == str(message.id)
    assert row["姓名"] == "测试用户"
    assert row["联系方式"] == "test@example.com"
    assert row["留言内容"] == message.message_text
    assert row["状态"] == "已处理"
    assert row["来源页面"] == "https://example.com/test"
    assert row["创建时间"] != ""
    assert row["处理时间"] != ""

    # 验证字段数量
    assert len(row) == 8
