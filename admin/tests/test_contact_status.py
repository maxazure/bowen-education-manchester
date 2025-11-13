"""
测试留言状态管理功能
"""

from datetime import datetime

from sqlalchemy.orm import Session

from app.models.contact import ContactMessage


def test_mark_as_read(db_session: Session):
    """测试标记为已读"""
    # 创建未读留言
    msg = ContactMessage(
        name="测试用户",
        contact_info="test@example.com",
        message_text="测试留言内容",
        status="unread",
    )
    db_session.add(msg)
    db_session.commit()

    # 验证初始状态
    assert msg.status == "unread"
    assert msg.handled_at is None

    # 标记为已处理
    msg.status = "handled"
    msg.handled_at = datetime.now()
    db_session.commit()

    # 验证状态已更新
    updated_msg = (
        db_session.query(ContactMessage).filter(ContactMessage.id == msg.id).first()
    )
    assert updated_msg.status == "handled"
    assert updated_msg.handled_at is not None


def test_mark_as_replied(db_session: Session):
    """测试标记为已回复"""
    # 创建未读留言
    msg = ContactMessage(
        name="测试用户",
        contact_info="test@example.com",
        message_text="我有一个问题需要咨询",
        status="unread",
    )
    db_session.add(msg)
    db_session.commit()

    # 标记为已处理（在实际应用中，可以添加 reply_text 字段来记录回复内容）
    msg.status = "handled"
    msg.handled_at = datetime.now()
    db_session.commit()

    # 验证状态
    updated_msg = (
        db_session.query(ContactMessage).filter(ContactMessage.id == msg.id).first()
    )
    assert updated_msg.status == "handled"
    assert updated_msg.handled_at is not None


def test_mark_as_archived(db_session: Session):
    """测试标记为已归档"""
    # 创建已处理的留言
    msg = ContactMessage(
        name="测试用户",
        contact_info="test@example.com",
        message_text="测试留言内容",
        status="handled",
        handled_at=datetime.now(),
    )
    db_session.add(msg)
    db_session.commit()

    # 在这个简单的实现中，我们使用 handled 状态来表示已处理/归档
    # 如果需要更复杂的归档逻辑，可以在未来扩展
    assert msg.status == "handled"
    assert msg.handled_at is not None

    # 也可以将留言标记回未读状态（取消归档）
    msg.status = "unread"
    msg.handled_at = None
    db_session.commit()

    updated_msg = (
        db_session.query(ContactMessage).filter(ContactMessage.id == msg.id).first()
    )
    assert updated_msg.status == "unread"
    assert updated_msg.handled_at is None


def test_batch_mark(db_session: Session):
    """测试批量标记状态"""
    # 创建多条未读留言
    messages = []
    for i in range(5):
        msg = ContactMessage(
            name=f"用户 {i}",
            contact_info=f"user{i}@example.com",
            message_text=f"留言内容 {i}",
            status="unread",
        )
        messages.append(msg)
    db_session.add_all(messages)
    db_session.commit()

    # 获取所有留言的ID
    msg_ids = [msg.id for msg in messages]

    # 批量标记为已处理
    handled_time = datetime.now()
    db_session.query(ContactMessage).filter(ContactMessage.id.in_(msg_ids)).update(
        {"status": "handled", "handled_at": handled_time}, synchronize_session=False
    )
    db_session.commit()

    # 验证所有留言都已标记为已处理
    updated_messages = (
        db_session.query(ContactMessage).filter(ContactMessage.id.in_(msg_ids)).all()
    )
    assert len(updated_messages) == 5
    assert all(msg.status == "handled" for msg in updated_messages)
    assert all(msg.handled_at is not None for msg in updated_messages)

    # 测试批量标记回未读
    db_session.query(ContactMessage).filter(
        ContactMessage.id.in_(msg_ids[:3])  # 只标记前3条
    ).update({"status": "unread", "handled_at": None}, synchronize_session=False)
    db_session.commit()

    # 验证前3条是未读，后2条仍是已处理
    all_messages = (
        db_session.query(ContactMessage)
        .filter(ContactMessage.id.in_(msg_ids))
        .order_by(ContactMessage.id)
        .all()
    )

    assert all_messages[0].status == "unread"
    assert all_messages[1].status == "unread"
    assert all_messages[2].status == "unread"
    assert all_messages[3].status == "handled"
    assert all_messages[4].status == "handled"
