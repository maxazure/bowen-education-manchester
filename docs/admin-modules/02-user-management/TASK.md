# 模块 02: 用户管理

**模块编号**: 02
**模块名称**: User Management
**优先级**: P0 (最高)
**预计工时**: 2 天
**负责 Subagent**: user-management
**依赖**: 模块 01 (基础设施搭建)

---

## 📋 任务概述

实现管理后台的用户认证系统，包括管理员登录、登出、Session 管理、密码修改等核心功能。这是管理后台安全的基础模块。

---

## 🎯 任务目标

1. ✅ 创建管理员数据模型
2. ✅ 实现登录/登出功能
3. ✅ 实现 Session 管理
4. ✅ 实现认证中间件
5. ✅ 实现密码修改功能
6. ✅ 创建初始管理员账号

---

## 🗄️ 数据库设计

### admin_users 表

```sql
CREATE TABLE admin_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    last_login_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 索引
CREATE UNIQUE INDEX idx_admin_username ON admin_users(username);
CREATE UNIQUE INDEX idx_admin_email ON admin_users(email);
```

### 字段说明

| 字段 | 类型 | 说明 | 约束 |
|-----|------|------|------|
| id | INTEGER | 主键 | PRIMARY KEY |
| username | VARCHAR(50) | 用户名 | UNIQUE, NOT NULL |
| password_hash | VARCHAR(255) | 密码哈希 | NOT NULL |
| email | VARCHAR(100) | 邮箱 | UNIQUE, NOT NULL |
| last_login_at | TIMESTAMP | 最后登录时间 | NULL |
| created_at | TIMESTAMP | 创建时间 | DEFAULT NOW |
| updated_at | TIMESTAMP | 更新时间 | ON UPDATE NOW |

---

## ✅ TDD 测试用例

### 测试文件: `tests/admin/test_auth.py`

```python
"""
用户认证测试
"""
import pytest
from fastapi.testclient import TestClient
from app.models.admin_user import AdminUser


class TestAdminUserModel:
    """测试管理员模型"""

    def test_create_admin_user(self, db_session):
        """测试创建管理员"""
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

    def test_password_hashing(self, db_session):
        """测试密码加密"""
        admin = AdminUser(
            username="testadmin",
            email="test@example.com"
        )
        admin.set_password("password123")

        # 密码不应该明文存储
        assert admin.password_hash != "password123"
        # 密码哈希应该是 bcrypt 格式
        assert admin.password_hash.startswith("$2b$")

    def test_password_verification(self, db_session):
        """测试密码验证"""
        admin = AdminUser(
            username="testadmin",
            email="test@example.com"
        )
        admin.set_password("password123")

        # 正确密码应该验证成功
        assert admin.verify_password("password123") is True
        # 错误密码应该验证失败
        assert admin.verify_password("wrongpassword") is False

    def test_username_unique(self, db_session):
        """测试用户名唯一性"""
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

    def test_email_unique(self, db_session):
        """测试邮箱唯一性"""
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

    def test_login_page_loads(self, client):
        """测试登录页面加载"""
        response = client.get("/admin/login")
        assert response.status_code == 200
        assert b"login" in response.content.lower()

    def test_login_with_valid_credentials(self, client, db_session):
        """测试使用正确凭据登录"""
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

    def test_login_with_invalid_username(self, client):
        """测试使用错误用户名登录"""
        response = client.post("/admin/login", data={
            "username": "nonexistent",
            "password": "password123"
        })

        assert response.status_code == 200
        assert b"用户名或密码错误" in response.content or b"Invalid" in response.content

    def test_login_with_invalid_password(self, client, db_session):
        """测试使用错误密码登录"""
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
        assert b"用户名或密码错误" in response.content or b"Invalid" in response.content

    def test_logout(self, client, db_session):
        """测试登出"""
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

    def test_admin_pages_require_login(self, client):
        """测试管理页面需要登录"""
        # 未登录访问仪表板
        response = client.get("/admin/", follow_redirects=False)

        # 应该重定向到登录页
        assert response.status_code == 302
        assert "/admin/login" in response.headers["location"]

    def test_login_page_accessible_without_auth(self, client):
        """测试登录页面无需认证"""
        response = client.get("/admin/login")
        assert response.status_code == 200

    def test_authenticated_user_can_access_admin(self, client, db_session):
        """测试已认证用户可以访问管理页面"""
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

    def test_change_password_page_loads(self, client, db_session):
        """测试密码修改页面加载"""
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

    def test_change_password_with_correct_old_password(self, client, db_session):
        """测试使用正确的旧密码修改密码"""
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

    def test_change_password_with_wrong_old_password(self, client, db_session):
        """测试使用错误的旧密码修改密码"""
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
        assert b"旧密码错误" in response.content or b"incorrect" in response.content.lower()

    def test_change_password_with_mismatched_confirmation(self, client, db_session):
        """测试新密码和确认密码不一致"""
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
        assert b"密码不一致" in response.content or b"not match" in response.content.lower()


class TestSessionManagement:
    """测试 Session 管理"""

    def test_session_created_on_login(self, client, db_session):
        """测试登录时创建 Session"""
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

    def test_session_cleared_on_logout(self, client, db_session):
        """测试登出时清除 Session"""
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
        response = client.get("/admin/logout")

        # 登出后不能访问管理页面
        response = client.get("/admin/", follow_redirects=False)
        assert response.status_code == 302

    def test_last_login_time_updated(self, client, db_session):
        """测试登录时更新最后登录时间"""
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
```

**测试统计**:
- 测试类: 5 个
- 测试用例: 22 个
- 预期全部通过

---

## 📝 开发步骤（TDD）

### Step 1: 编写测试 (Red)

```bash
# 创建测试文件
touch tests/admin/test_auth.py

# 编写所有测试用例
# 运行测试（预期失败）
pytest tests/admin/test_auth.py -v
```

### Step 2: 创建数据模型 (Green)

```bash
# 创建管理员模型
touch app/models/admin_user.py

# 编写 AdminUser 模型类
# 包含: 字段定义、set_password()、verify_password()
```

### Step 3: 创建数据库迁移

```bash
# 生成迁移文件
alembic revision --autogenerate -m "add admin_users table"

# 执行迁移
alembic upgrade head
```

### Step 4: 实现登录路由

```bash
# 创建认证路由
touch app/admin/routers/auth.py

# 实现:
# - GET /admin/login (登录页面)
# - POST /admin/login (登录处理)
# - GET /admin/logout (登出)
```

### Step 5: 实现 Session 管理

```bash
# 配置 Session 中间件
# 在 main.py 中添加 SessionMiddleware
# 设置 SECRET_KEY
```

### Step 6: 实现认证中间件 (Green)

```bash
# 编辑 app/admin/middleware.py
# 实现 AdminAuthMiddleware
# 检查 session 中的 admin_user_id
```

### Step 7: 实现密码修改功能

```bash
# 在 app/admin/routers/auth.py 添加:
# - GET /admin/profile/change-password (密码修改页面)
# - POST /admin/profile/change-password (密码修改处理)
```

### Step 8: 创建模板

```bash
# 创建登录页面模板
touch templates/admin/login.html

# 创建密码修改页面模板
touch templates/admin/profile/change-password.html
```

### Step 9: 创建初始化脚本

```bash
# 创建管理员初始化脚本
touch scripts/init_admin.py

# 实现创建默认管理员功能
```

### Step 10: 运行测试验证 (Green)

```bash
# 再次运行测试（预期全部通过）
pytest tests/admin/test_auth.py -v

# 查看覆盖率
pytest tests/admin/test_auth.py --cov=app/admin --cov-report=html
```

### Step 11: 重构和优化 (Refactor)

```bash
# 代码格式化
black app/admin/ app/models/
isort app/admin/ app/models/

# 类型检查
mypy app/admin/ app/models/

# 代码检查
ruff check app/admin/ app/models/
```

---

## 📄 核心代码实现

### `app/models/admin_user.py`

```python
"""
管理员用户模型
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base
import bcrypt


class AdminUser(Base):
    """管理员用户表"""

    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def set_password(self, password: str) -> None:
        """
        设置密码（自动哈希）

        Args:
            password: 明文密码
        """
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(
            password.encode('utf-8'),
            salt
        ).decode('utf-8')

    def verify_password(self, password: str) -> bool:
        """
        验证密码

        Args:
            password: 明文密码

        Returns:
            bool: 密码是否正确
        """
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )

    def __repr__(self) -> str:
        return f"<AdminUser(id={self.id}, username='{self.username}')>"
```

### `app/admin/routers/auth.py`

```python
"""
管理后台认证路由
"""
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.database import get_db
from app.models.admin_user import AdminUser

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """
    登录页面
    """
    return templates.TemplateResponse(
        "admin/login.html",
        {"request": request}
    )


@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    登录处理
    """
    # 查询管理员
    admin = db.query(AdminUser).filter(
        AdminUser.username == username
    ).first()

    # 验证用户名和密码
    if not admin or not admin.verify_password(password):
        return templates.TemplateResponse(
            "admin/login.html",
            {
                "request": request,
                "error": "用户名或密码错误"
            }
        )

    # 更新最后登录时间
    admin.last_login_at = func.now()
    db.commit()

    # 设置 Session
    request.session["admin_user_id"] = admin.id
    request.session["admin_username"] = admin.username

    # 重定向到仪表板
    return RedirectResponse(url="/admin/", status_code=302)


@router.get("/logout")
async def logout(request: Request):
    """
    登出
    """
    # 清除 Session
    request.session.clear()

    # 重定向到登录页
    return RedirectResponse(url="/admin/login", status_code=302)


@router.get("/profile/change-password", response_class=HTMLResponse)
async def change_password_page(request: Request):
    """
    密码修改页面
    """
    return templates.TemplateResponse(
        "admin/profile/change-password.html",
        {"request": request}
    )


@router.post("/profile/change-password")
async def change_password(
    request: Request,
    old_password: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    密码修改处理
    """
    # 获取当前用户
    admin_user_id = request.session.get("admin_user_id")
    admin = db.query(AdminUser).filter(AdminUser.id == admin_user_id).first()

    # 验证旧密码
    if not admin.verify_password(old_password):
        return templates.TemplateResponse(
            "admin/profile/change-password.html",
            {
                "request": request,
                "error": "旧密码错误"
            }
        )

    # 验证新密码一致性
    if new_password != confirm_password:
        return templates.TemplateResponse(
            "admin/profile/change-password.html",
            {
                "request": request,
                "error": "两次输入的新密码不一致"
            }
        )

    # 更新密码
    admin.set_password(new_password)
    db.commit()

    # 重定向到仪表板
    return RedirectResponse(url="/admin/", status_code=302)
```

### `app/admin/middleware.py` (更新)

```python
"""
管理后台中间件
"""
from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware


class AdminAuthMiddleware(BaseHTTPMiddleware):
    """
    管理后台认证中间件

    检查用户是否已登录，未登录则重定向到登录页。
    """

    async def dispatch(self, request: Request, call_next):
        # 公开路径（无需认证）
        public_paths = ["/admin/login"]
        static_paths = ["/static/", "/uploads/"]

        # 检查是否是静态资源
        for static_path in static_paths:
            if request.url.path.startswith(static_path):
                response = await call_next(request)
                return response

        # 如果是管理后台路径且不是公开路径
        if (request.url.path.startswith("/admin") and
            request.url.path not in public_paths):
            # 检查 session 中是否有用户信息
            user_id = request.session.get("admin_user_id")
            if not user_id:
                # 未登录，重定向到登录页
                if request.method == "GET":
                    return RedirectResponse(url="/admin/login", status_code=302)
                else:
                    # POST 请求返回 401
                    from fastapi.responses import JSONResponse
                    return JSONResponse(
                        {"detail": "未授权"},
                        status_code=401
                    )

        response = await call_next(request)
        return response
```

### `scripts/init_admin.py`

```python
"""
初始化管理员账号

使用方法: python scripts/init_admin.py
"""
from app.database import SessionLocal
from app.models.admin_user import AdminUser


def init_admin():
    """创建初始管理员账号"""
    db = SessionLocal()

    try:
        # 检查是否已有管理员
        existing = db.query(AdminUser).filter_by(username="admin").first()
        if existing:
            print("❌ 管理员账号已存在")
            print(f"   用户名: {existing.username}")
            print(f"   邮箱: {existing.email}")
            return

        # 创建初始管理员
        admin = AdminUser(
            username="admin",
            email="admin@boweneducation.org"
        )
        admin.set_password("admin123")

        db.add(admin)
        db.commit()

        print("✅ 初始管理员账号创建成功")
        print("")
        print("   用户名: admin")
        print("   密码: admin123")
        print("   邮箱: admin@boweneducation.org")
        print("")
        print("⚠️  请在首次登录后立即修改密码！")

    except Exception as e:
        print(f"❌ 创建失败: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_admin()
```

### `templates/admin/login.html`

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>登录 - 博文教育集团管理后台</title>

    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .login-card {
            max-width: 400px;
            width: 100%;
        }
        .login-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        .login-header h1 {
            color: white;
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }
        .login-header p {
            color: rgba(255, 255, 255, 0.8);
        }
    </style>
</head>
<body>
    <div class="login-card">
        <div class="login-header">
            <h1>博文教育集团</h1>
            <p>管理后台</p>
        </div>

        <div class="card shadow-lg">
            <div class="card-body p-4">
                <h5 class="card-title text-center mb-4">登录</h5>

                {% if error %}
                <div class="alert alert-danger" role="alert">
                    {{ error }}
                </div>
                {% endif %}

                <form method="POST" action="/admin/login">
                    <div class="mb-3">
                        <label for="username" class="form-label">用户名</label>
                        <input type="text" class="form-control" id="username"
                               name="username" required autofocus>
                    </div>

                    <div class="mb-3">
                        <label for="password" class="form-label">密码</label>
                        <input type="password" class="form-control" id="password"
                               name="password" required>
                    </div>

                    <div class="d-grid">
                        <button type="submit" class="btn btn-primary">登录</button>
                    </div>
                </form>
            </div>
        </div>

        <div class="text-center mt-3">
            <small class="text-white">
                &copy; 2025 博文教育集团. All rights reserved.
            </small>
        </div>
    </div>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

---

## ✅ 完成标准

### 功能性要求

- [ ] AdminUser 模型创建完成
- [ ] 密码加密功能正常
- [ ] 密码验证功能正常
- [ ] 登录页面可访问
- [ ] 登录功能正常
- [ ] 登出功能正常
- [ ] Session 管理正常
- [ ] 认证中间件工作正常
- [ ] 密码修改功能正常
- [ ] 初始管理员创建成功
- [ ] 所有测试通过 (22/22)

### 质量要求

- [ ] 代码符合 PEP 8 规范
- [ ] 所有函数有类型提示
- [ ] 所有函数有文档字符串
- [ ] 测试覆盖率 >= 90%
- [ ] 无安全漏洞

### 安全要求

- [ ] 密码使用 bcrypt 加密
- [ ] Session 使用 HTTPOnly Cookie
- [ ] 未授权用户不能访问管理页面
- [ ] 密码不在日志中显示
- [ ] SQL 注入防护有效

### 文档要求

- [ ] 更新 TODO.md 记录完成情况
- [ ] 所有代码有清晰注释
- [ ] 创建使用说明文档

---

## 📊 验证命令

```bash
# 1. 创建数据库迁移
alembic revision --autogenerate -m "add admin_users table"
alembic upgrade head

# 2. 创建初始管理员
python scripts/init_admin.py

# 3. 运行测试
pytest tests/admin/test_auth.py -v

# 4. 查看覆盖率
pytest tests/admin/test_auth.py --cov=app/admin --cov=app/models --cov-report=term-missing

# 5. 代码质量检查
black app/admin/ app/models/ --check
isort app/admin/ app/models/ --check
mypy app/admin/ app/models/

# 6. 启动服务器测试
uvicorn main:app --reload

# 7. 手动测试登录
# 访问 http://localhost:8000/admin/login
# 用户名: admin
# 密码: admin123
```

---

## 🔄 交付物

1. ✅ AdminUser 模型（带密码加密）
2. ✅ 认证路由（登录/登出/密码修改）
3. ✅ 认证中间件（完整实现）
4. ✅ 登录页面模板
5. ✅ 密码修改页面模板
6. ✅ 初始化脚本
7. ✅ 数据库迁移文件
8. ✅ 22 个通过的测试用例
9. ✅ 更新的 TODO.md

---

## 📝 注意事项

1. **安全性**: 密码必须使用 bcrypt 加密，不能明文存储
2. **Session**: 必须配置 SECRET_KEY，不能使用默认值
3. **中间件**: 确保正确配置路由优先级，避免循环重定向
4. **测试**: 使用测试数据库，不要影响开发数据库
5. **初始密码**: 首次登录后必须提示用户修改密码

---

## 🔗 相关文档

- [admin-system-design.md](../../admin-system-design.md) - 系统设计文档 (第 44-61 行)
- [admin-development-plan.md](../../admin-development-plan.md) - 总体开发计划
- [TODO.md](./TODO.md) - 本模块待办事项
- [模块 01: 基础设施搭建](../01-infrastructure-setup/TASK.md) - 前置依赖
