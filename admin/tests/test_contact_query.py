"""
测试留言查询功能
"""


from sqlalchemy.orm import Session

from app.models.contact import ContactMessage


def test_get_list(db_session: Session):
    """测试获取留言列表"""
    # 创建多条留言
    messages = []
    for i in range(5):
        msg = ContactMessage(
            name=f"测试用户 {i}",
            contact_info=f"user{i}@example.com",
            message_text=f"这是第 {i} 条留言内容",
            status="unread" if i % 2 == 0 else "handled",
        )
        messages.append(msg)
    db_session.add_all(messages)
    db_session.commit()

    # 获取所有留言
    all_messages = db_session.query(ContactMessage).all()
    assert len(all_messages) == 5

    # 按创建时间降序排列
    ordered = (
        db_session.query(ContactMessage)
        .order_by(ContactMessage.created_at.desc())
        .all()
    )
    assert len(ordered) == 5
    # 最新的留言应该在前面
    for i in range(len(ordered) - 1):
        assert ordered[i].created_at >= ordered[i + 1].created_at


def test_filter_by_status(db_session: Session):
    """测试按状态筛选"""
    # 创建不同状态的留言
    msg1 = ContactMessage(
        name="用户A",
        contact_info="usera@example.com",
        message_text="未读留言",
        status="unread",
    )
    msg2 = ContactMessage(
        name="用户B",
        contact_info="userb@example.com",
        message_text="已处理留言",
        status="handled",
    )
    msg3 = ContactMessage(
        name="用户C",
        contact_info="userc@example.com",
        message_text="另一条未读留言",
        status="unread",
    )
    db_session.add_all([msg1, msg2, msg3])
    db_session.commit()

    # 筛选未读留言
    unread = (
        db_session.query(ContactMessage).filter(ContactMessage.status == "unread").all()
    )
    assert len(unread) == 2
    assert all(msg.status == "unread" for msg in unread)

    # 筛选已处理留言
    handled = (
        db_session.query(ContactMessage)
        .filter(ContactMessage.status == "handled")
        .all()
    )
    assert len(handled) == 1
    assert handled[0].name == "用户B"


def test_keyword_search(db_session: Session):
    """测试关键词搜索"""
    # 创建留言
    msg1 = ContactMessage(
        name="张三",
        contact_info="zhangsan@example.com",
        message_text="我想咨询羽毛球课程的价格",
        status="unread",
    )
    msg2 = ContactMessage(
        name="李四",
        contact_info="lisi@example.com",
        message_text="请问有周末的培训班吗？",
        status="unread",
    )
    msg3 = ContactMessage(
        name="王五",
        contact_info="wangwu@example.com",
        message_text="羽毛球拍的价格是多少？",
        status="handled",
    )
    db_session.add_all([msg1, msg2, msg3])
    db_session.commit()

    # 按姓名搜索
    keyword = "张三"
    results = (
        db_session.query(ContactMessage)
        .filter(ContactMessage.name.contains(keyword))
        .all()
    )
    assert len(results) == 1
    assert results[0].name == "张三"

    # 按联系方式搜索
    keyword = "lisi"
    results = (
        db_session.query(ContactMessage)
        .filter(ContactMessage.contact_info.contains(keyword))
        .all()
    )
    assert len(results) == 1
    assert results[0].name == "李四"

    # 按留言内容搜索
    keyword = "羽毛球"
    results = (
        db_session.query(ContactMessage)
        .filter(ContactMessage.message_text.contains(keyword))
        .all()
    )
    assert len(results) == 2
    names = [msg.name for msg in results]
    assert "张三" in names
    assert "王五" in names

    # 组合搜索（姓名、联系方式、留言内容）
    keyword = "example.com"
    results = (
        db_session.query(ContactMessage)
        .filter(
            (ContactMessage.name.contains(keyword))
            | (ContactMessage.contact_info.contains(keyword))
            | (ContactMessage.message_text.contains(keyword))
        )
        .all()
    )
    assert len(results) == 3


def test_pagination(db_session: Session):
    """测试分页"""
    # 创建25条留言
    messages = []
    for i in range(1, 26):
        msg = ContactMessage(
            name=f"用户 {i}",
            contact_info=f"user{i}@example.com",
            message_text=f"留言内容 {i}",
            status="unread",
        )
        messages.append(msg)
    db_session.add_all(messages)
    db_session.commit()

    # 测试第1页（每页20条）
    page_size = 20
    page1 = (
        db_session.query(ContactMessage)
        .order_by(ContactMessage.created_at.desc())
        .limit(page_size)
        .offset(0)
        .all()
    )
    assert len(page1) == 20

    # 测试第2页
    page2 = (
        db_session.query(ContactMessage)
        .order_by(ContactMessage.created_at.desc())
        .limit(page_size)
        .offset(20)
        .all()
    )
    assert len(page2) == 5

    # 测试总数
    total = db_session.query(ContactMessage).count()
    assert total == 25

    # 计算总页数
    import math

    total_pages = math.ceil(total / page_size)
    assert total_pages == 2
