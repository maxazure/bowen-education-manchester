"""
用户认证测试

严格遵循 TDD 流程编写的测试用例
共 5 个测试类，22 个测试用例
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


class TestAdminUserModel:
    """测试管理员模型"""

    def test_create_admin_user(self, db_session: Session):
        """测试创建管理员"""
        from app.models.admin_user import AdminUser

        admin = AdminUser(
            username="testadmin",
            email="test@example.com"
        )
        admin.set_password("password123")

        db_session.add(admin)
        db_session.commit()

        assert admin.id is not None
        assert admin.username == "testadmin"
        assert admin.email == "test@example.com"
        assert admin.password_hash is not None

    def test_password_hashing(self, db_session: Session):
        """测试密码加密"""
        from app.models.admin_user import AdminUser

        admin = AdminUser(
            username="testadmin",
            email="test@example.com"
        )
        admin.set_password("password123")

        # 密码不应该明文存储
        assert admin.password_hash != "password123"
        # 密码哈希应该是 bcrypt 格式
        assert admin.password_hash.startswith("$2b$")

    def test_password_verification(self, db_session: Session):
        """测试密码验证"""
        from app.models.admin_user import AdminUser

        admin = AdminUser(
            username="testadmin",
            email="test@example.com"
        )
        admin.set_password("password123")

        # 正确密码应该验证成功
        assert admin.verify_password("password123") is True
        # 错误密码应该验证失败
        assert admin.verify_password("wrongpassword") is False

    def test_username_unique(self, db_session: Session):
        """测试用户名唯一性"""
        from app.models.admin_user import AdminUser

        admin1 = AdminUser(
            username="testadmin",
            email="test1@example.com"
        )
        admin1.set_password("password123")
        db_session.add(admin1)
        db_session.commit()

        # 尝试创建相同用户名
        admin2 = AdminUser(
            username="testadmin",
            email="test2@example.com"
        )
        admin2.set_password("password123")
        db_session.add(admin2)

        with pytest.raises(Exception):  # IntegrityError
            db_session.commit()

    def test_email_unique(self, db_session: Session):
        """测试邮箱唯一性"""
        from app.models.admin_user import AdminUser

        admin1 = AdminUser(
            username="testadmin1",
            email="test@example.com"
        )
        admin1.set_password("password123")
        db_session.add(admin1)
        db_session.commit()

        # 尝试创建相同邮箱
        admin2 = AdminUser(
            username="testadmin2",
            email="test@example.com"
        )
        admin2.set_password("password123")
        db_session.add(admin2)

        with pytest.raises(Exception):  # IntegrityError
            db_session.commit()


class TestLoginLogout:
    """测试登录登出"""

    def test_login_page_loads(self, client: TestClient):
        """测试登录页面加载"""
        response = client.get("/admin/login")
        assert response.status_code == 200
        assert b"login" in response.content.lower()

    def test_login_with_valid_credentials(self, client: TestClient, db_session: Session):
        """测试使用正确凭据登录"""
        from app.models.admin_user import AdminUser

        # 创建测试管理员
        admin = AdminUser(
            username="testadmin",
            email="test@example.com"
        )
        admin.set_password("password123")
        db_session.add(admin)
        db_session.commit()

        # 登录
        response = client.post("/admin/login", data={
            "username": "testadmin",
            "password": "password123"
        }, follow_redirects=False)

        # 应该重定向到仪表板
        assert response.status_code == 302
        assert response.headers["location"] == "/admin/"

    def test_login_with_invalid_username(self, client: TestClient):
        """测试使用错误用户名登录"""
        response = client.post("/admin/login", data={
            "username": "nonexistent",
            "password": "password123"
        })

        assert response.status_code == 200
        assert b"\xe7\x94\xa8\xe6\x88\xb7\xe5\x90\x8d\xe6\x88\x96\xe5\xaf\x86\xe7\xa0\x81\xe9\x94\x99\xe8\xaf\xaf" in response.content or b"Invalid" in response.content

    def test_login_with_invalid_password(self, client: TestClient, db_session: Session):
        """测试使用错误密码登录"""
        from app.models.admin_user import AdminUser

        # 创建测试管理员
        admin = AdminUser(
            username="testadmin",
            email="test@example.com"
        )
        admin.set_password("password123")
        db_session.add(admin)
        db_session.commit()

        # 使用错误密码登录
        response = client.post("/admin/login", data={
            "username": "testadmin",
            "password": "wrongpassword"
        })

        assert response.status_code == 200
        assert b"\xe7\x94\xa8\xe6\x88\xb7\xe5\x90\x8d\xe6\x88\x96\xe5\xaf\x86\xe7\xa0\x81\xe9\x94\x99\xe8\xaf\xaf" in response.content or b"Invalid" in response.content

    def test_logout(self, client: TestClient, db_session: Session):
        """测试登出"""
        from app.models.admin_user import AdminUser

        # 先登录
        admin = AdminUser(
            username="testadmin",
            email="test@example.com"
        )
        admin.set_password("password123")
        db_session.add(admin)
        db_session.commit()

        client.post("/admin/login", data={
            "username": "testadmin",
            "password": "password123"
        })

        # 登出
        response = client.get("/admin/logout", follow_redirects=False)

        # 应该重定向到登录页
        assert response.status_code == 302
        assert response.headers["location"] == "/admin/login"


class TestAuthMiddleware:
    """测试认证中间件"""

    def test_admin_pages_require_login(self, client: TestClient):
        """测试管理页面需要登录"""
        # 未登录访问仪表板
        response = client.get("/admin/", follow_redirects=False)

        # 应该重定向到登录页
        assert response.status_code == 302
        assert "/admin/login" in response.headers["location"]

    def test_login_page_accessible_without_auth(self, client: TestClient):
        """测试登录页面无需认证"""
        response = client.get("/admin/login")
        assert response.status_code == 200

    def test_authenticated_user_can_access_admin(self, client: TestClient, db_session: Session):
        """测试已认证用户可以访问管理页面"""
        from app.models.admin_user import AdminUser

        # 创建并登录
        admin = AdminUser(
            username="testadmin",
            email="test@example.com"
        )
        admin.set_password("password123")
        db_session.add(admin)
        db_session.commit()

        client.post("/admin/login", data={
            "username": "testadmin",
            "password": "password123"
        })

        # 访问仪表板
        response = client.get("/admin/")
        assert response.status_code == 200


class TestPasswordChange:
    """测试密码修改"""

    def test_change_password_page_loads(self, client: TestClient, db_session: Session):
        """测试密码修改页面加载"""
        from app.models.admin_user import AdminUser

        # 先登录
        admin = AdminUser(
            username="testadmin",
            email="test@example.com"
        )
        admin.set_password("password123")
        db_session.add(admin)
        db_session.commit()

        client.post("/admin/login", data={
            "username": "testadmin",
            "password": "password123"
        })

        # 访问密码修改页面
        response = client.get("/admin/profile/change-password")
        assert response.status_code == 200

    def test_change_password_with_correct_old_password(self, client: TestClient, db_session: Session):
        """测试使用正确的旧密码修改密码"""
        from app.models.admin_user import AdminUser

        # 创建并登录
        admin = AdminUser(
            username="testadmin",
            email="test@example.com"
        )
        admin.set_password("oldpassword")
        db_session.add(admin)
        db_session.commit()

        client.post("/admin/login", data={
            "username": "testadmin",
            "password": "oldpassword"
        })

        # 修改密码
        response = client.post("/admin/profile/change-password", data={
            "old_password": "oldpassword",
            "new_password": "newpassword123",
            "confirm_password": "newpassword123"
        })

        assert response.status_code == 302  # 重定向表示成功

        # 验证新密码可以登录
        client.get("/admin/logout")
        response = client.post("/admin/login", data={
            "username": "testadmin",
            "password": "newpassword123"
        }, follow_redirects=False)

        assert response.status_code == 302

    def test_change_password_with_wrong_old_password(self, client: TestClient, db_session: Session):
        """测试使用错误的旧密码修改密码"""
        from app.models.admin_user import AdminUser

        # 创建并登录
        admin = AdminUser(
            username="testadmin",
            email="test@example.com"
        )
        admin.set_password("password123")
        db_session.add(admin)
        db_session.commit()

        client.post("/admin/login", data={
            "username": "testadmin",
            "password": "password123"
        })

        # 使用错误的旧密码
        response = client.post("/admin/profile/change-password", data={
            "old_password": "wrongpassword",
            "new_password": "newpassword123",
            "confirm_password": "newpassword123"
        })

        assert response.status_code == 200
        assert b"\xe6\x97\xa7\xe5\xaf\x86\xe7\xa0\x81\xe9\x94\x99\xe8\xaf\xaf" in response.content or b"incorrect" in response.content.lower()

    def test_change_password_with_mismatched_confirmation(self, client: TestClient, db_session: Session):
        """测试新密码和确认密码不一致"""
        from app.models.admin_user import AdminUser

        # 创建并登录
        admin = AdminUser(
            username="testadmin",
            email="test@example.com"
        )
        admin.set_password("password123")
        db_session.add(admin)
        db_session.commit()

        client.post("/admin/login", data={
            "username": "testadmin",
            "password": "password123"
        })

        # 新密码和确认密码不一致
        response = client.post("/admin/profile/change-password", data={
            "old_password": "password123",
            "new_password": "newpassword123",
            "confirm_password": "differentpassword"
        })

        assert response.status_code == 200
        assert b"\xe5\xaf\x86\xe7\xa0\x81\xe4\xb8\x8d\xe4\xb8\x80\xe8\x87\xb4" in response.content or b"not match" in response.content.lower()


class TestSessionManagement:
    """测试 Session 管理"""

    def test_session_created_on_login(self, client: TestClient, db_session: Session):
        """测试登录时创建 Session"""
        from app.models.admin_user import AdminUser

        admin = AdminUser(
            username="testadmin",
            email="test@example.com"
        )
        admin.set_password("password123")
        db_session.add(admin)
        db_session.commit()

        response = client.post("/admin/login", data={
            "username": "testadmin",
            "password": "password123"
        })

        # 检查是否设置了 Cookie
        assert "session" in response.cookies or "Set-Cookie" in response.headers

    def test_session_cleared_on_logout(self, client: TestClient, db_session: Session):
        """测试登出时清除 Session"""
        from app.models.admin_user import AdminUser

        # 先登录
        admin = AdminUser(
            username="testadmin",
            email="test@example.com"
        )
        admin.set_password("password123")
        db_session.add(admin)
        db_session.commit()

        client.post("/admin/login", data={
            "username": "testadmin",
            "password": "password123"
        })

        # 登出
        client.get("/admin/logout")

        # 登出后不能访问管理页面
        response = client.get("/admin/", follow_redirects=False)
        assert response.status_code == 302

    def test_last_login_time_updated(self, client: TestClient, db_session: Session):
        """测试登录时更新最后登录时间"""
        from app.models.admin_user import AdminUser

        admin = AdminUser(
            username="testadmin",
            email="test@example.com"
        )
        admin.set_password("password123")
        db_session.add(admin)
        db_session.commit()

        assert admin.last_login_at is None

        # 登录
        client.post("/admin/login", data={
            "username": "testadmin",
            "password": "password123"
        })

        # 刷新对象
        db_session.refresh(admin)

        # 最后登录时间应该被更新
        assert admin.last_login_at is not None
