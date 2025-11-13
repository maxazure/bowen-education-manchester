# 模块 01: 基础设施搭建（独立Admin目录版本）

**模块编号**: 01
**模块名称**: Infrastructure Setup
**优先级**: P0 (最高)
**预计工时**: 2 天
**负责 Subagent**: infrastructure-setup
**依赖**: 无

**版本**: v2.0 - 完全独立的admin目录结构
**更新日期**: 2025-11-13

---

## 📋 任务概述

搭建**完全独立**的管理后台系统基础架构。所有管理后台相关的代码、模板、静态资源都放在独立的 `admin/` 目录下，与前台系统完全隔离。

---

## 🎯 任务目标

1. ✅ 创建独立的 `admin/` 目录结构
2. ✅ 配置所有必需的依赖包
3. ✅ 建立完整的测试环境
4. ✅ 创建基础模板和静态资源框架
5. ✅ 创建独立的后台应用入口

---

## 📁 新的目录结构设计（完全独立）

```
admin/                          # 管理后台根目录（完全独立）
├── app/                        # 后台应用代码
│   ├── __init__.py             # 应用包初始化
│   ├── main.py                 # 后台应用入口（FastAPI app）
│   ├── config.py               # 后台配置
│   ├── database.py             # 数据库连接（引用主项目）
│   ├── models/                 # 后台数据模型
│   │   ├── __init__.py
│   │   └── (后续添加)
│   ├── routers/                # 后台路由
│   │   ├── __init__.py
│   │   └── (后续添加)
│   ├── services/               # 后台业务逻辑
│   │   └── __init__.py
│   ├── middleware.py           # 认证中间件
│   ├── dependencies.py         # 依赖注入
│   └── utils.py                # 工具函数
├── templates/                  # 后台模板（独立）
│   ├── base.html               # 基础布局模板
│   ├── login.html              # 登录页面
│   ├── dashboard.html          # 仪表板
│   └── components/             # 公共组件
│       ├── header.html
│       ├── sidebar.html
│       └── pagination.html
├── static/                     # 后台静态资源（独立）
│   ├── css/
│   │   └── admin.css
│   ├── js/
│   │   └── admin.js
│   └── images/
├── tests/                      # 后台测试
│   ├── __init__.py
│   ├── conftest.py             # pytest 配置
│   └── test_infrastructure.py  # 基础设施测试
├── uploads/                    # 上传文件目录
├── .gitignore                  # Git 忽略配置
└── README.md                   # 后台说明文档
```

---

## 🔄 与旧结构的对比

### 旧结构（已废弃）
```
app/admin/          # 代码在主项目的app下
templates/admin/    # 模板与前台混在一起
static/admin/       # 静态资源与前台混在一起
tests/admin/        # 测试与前台混在一起
```

### 新结构（推荐）
```
admin/              # 完全独立的目录
├── app/            # 独立的应用代码
├── templates/      # 独立的模板
├── static/         # 独立的静态资源
└── tests/          # 独立的测试
```

### 优势
1. ✅ **完全隔离** - 与前台代码零混淆
2. ✅ **独立部署** - 可以单独运行管理后台
3. ✅ **清晰结构** - 所有后台相关文件都在admin/下
4. ✅ **易于维护** - 修改后台不影响前台
5. ✅ **独立打包** - 可以单独打包管理后台

---

## 📦 依赖包清单

### 新增依赖（需要添加到项目根目录的 requirements.txt）

```txt
# 密码加密
bcrypt==4.1.2

# Session 管理
itsdangerous==2.1.2
starlette-session==0.3.0      # Session 中间件

# 图片处理
Pillow==11.0.0                # 升级支持 Python 3.13

# Markdown 处理
mistune==3.0.2

# 测试框架
pytest==8.3.4                 # 升级支持 Python 3.13
pytest-asyncio==0.25.2        # 升级支持 Python 3.13
pytest-cov==6.0.0             # 升级
httpx==0.28.1                 # 升级

# 代码质量
ruff==0.1.11

# ORM（升级）
sqlalchemy==2.0.36            # 升级支持 Python 3.13
alembic==1.14.0               # 升级
```

---

## 🧪 TDD 测试用例

### 测试文件: `admin/tests/test_infrastructure.py`

需要编写以下测试用例：

```python
"""
基础设施测试
"""
import os
import pytest
from pathlib import Path


class TestAdminDirectoryStructure:
    """测试admin目录结构"""

    def test_admin_root_exists(self):
        """测试 admin/ 根目录存在"""
        assert Path("admin").exists()
        assert Path("admin").is_dir()

    def test_admin_app_directory_exists(self):
        """测试 admin/app 目录存在"""
        assert Path("admin/app").exists()

    def test_admin_templates_directory_exists(self):
        """测试 admin/templates 目录存在"""
        assert Path("admin/templates").exists()

    def test_admin_static_directory_exists(self):
        """测试 admin/static 目录存在"""
        assert Path("admin/static").exists()

    def test_admin_tests_directory_exists(self):
        """测试 admin/tests 目录存在"""
        assert Path("admin/tests").exists()

    def test_admin_uploads_directory_exists(self):
        """测试 admin/uploads 目录存在"""
        assert Path("admin/uploads").exists()


class TestAdminDependencies:
    """测试依赖包"""

    def test_bcrypt_installed(self):
        """测试 bcrypt 已安装"""
        import bcrypt
        assert bcrypt is not None

    def test_pillow_installed(self):
        """测试 Pillow 已安装"""
        from PIL import Image
        assert Image is not None

    def test_mistune_installed(self):
        """测试 mistune 已安装"""
        import mistune
        assert mistune is not None

    def test_pytest_installed(self):
        """测试 pytest 已安装"""
        import pytest
        assert pytest is not None


class TestAdminPytestConfiguration:
    """测试 pytest 配置"""

    def test_pytest_ini_exists(self):
        """测试 pytest.ini 存在"""
        assert Path("pytest.ini").exists()

    def test_admin_conftest_exists(self):
        """测试 admin/tests/conftest.py 存在"""
        assert Path("admin/tests/conftest.py").exists()


class TestAdminBaseFiles:
    """测试基础文件"""

    def test_admin_app_init_exists(self):
        """测试 admin/app/__init__.py 存在"""
        assert Path("admin/app/__init__.py").exists()

    def test_admin_app_main_exists(self):
        """测试 admin/app/main.py 存在"""
        assert Path("admin/app/main.py").exists()

    def test_admin_middleware_exists(self):
        """测试 admin/app/middleware.py 存在"""
        assert Path("admin/app/middleware.py").exists()

    def test_admin_dependencies_exists(self):
        """测试 admin/app/dependencies.py 存在"""
        assert Path("admin/app/dependencies.py").exists()

    def test_admin_utils_exists(self):
        """测试 admin/app/utils.py 存在"""
        assert Path("admin/app/utils.py").exists()

    def test_admin_readme_exists(self):
        """测试 admin/README.md 存在"""
        assert Path("admin/README.md").exists()
```

**测试统计**:
- 测试类: 4 个
- 测试用例: 17 个
- 预期全部通过

---

## 📝 开发步骤（TDD）

### Step 1: 清理旧结构（如果存在）

```bash
# 备份并清理旧的混合结构
# 如果之前创建了 app/admin/, templates/admin/ 等，先删除
rm -rf app/admin
rm -rf templates/admin
rm -rf static/admin
rm -rf tests/admin
```

### Step 2: 编写测试 (Red)

```bash
# 创建测试文件
mkdir -p admin/tests
touch admin/tests/__init__.py
touch admin/tests/test_infrastructure.py

# 编写上述所有测试用例（17个）
# 运行测试（预期失败）
pytest admin/tests/test_infrastructure.py -v
```

### Step 3: 创建独立的admin目录结构 (Green)

```bash
# 创建admin根目录
mkdir -p admin

# 创建app目录和子目录
mkdir -p admin/app/{models,routers,services}

# 创建模板目录
mkdir -p admin/templates/components

# 创建静态资源目录
mkdir -p admin/static/{css,js,images}

# 创建测试目录
mkdir -p admin/tests

# 创建上传目录
mkdir -p admin/uploads
```

### Step 4: 创建基础Python文件

#### `admin/app/__init__.py`
```python
"""
博文教育管理后台应用

这是一个独立的FastAPI应用，用于管理博文教育网站的内容。
"""

__version__ = "1.0.0"
__author__ = "maxazure"
```

#### `admin/app/main.py`
```python
"""
管理后台应用入口

独立的FastAPI应用，可以单独运行。
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import os
from pathlib import Path

# 获取admin目录的绝对路径
ADMIN_DIR = Path(__file__).parent.parent

# 创建FastAPI应用
app = FastAPI(
    title="博文教育管理后台",
    description="Bowen Education Admin System",
    version="1.0.0"
)

# 添加Session中间件
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
)

# 挂载静态文件
app.mount(
    "/static",
    StaticFiles(directory=str(ADMIN_DIR / "static")),
    name="static"
)

# 配置模板
templates = Jinja2Templates(directory=str(ADMIN_DIR / "templates"))


@app.get("/")
async def root():
    """根路径"""
    return {"message": "博文教育管理后台API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "ok"}
```

#### `admin/app/config.py`
```python
"""
管理后台配置
"""
from pathlib import Path
import os

# 基础路径
ADMIN_DIR = Path(__file__).parent.parent
PROJECT_ROOT = ADMIN_DIR.parent

# 数据库配置（使用主项目的数据库）
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{PROJECT_ROOT}/app.db"
)

# Session 配置
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")
SESSION_COOKIE_NAME = "admin_session"
SESSION_MAX_AGE = 86400  # 24小时

# 上传配置
UPLOAD_DIR = ADMIN_DIR / "uploads"
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5MB

# 分页配置
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100
```

#### `admin/app/database.py`
```python
"""
数据库连接配置

复用主项目的数据库连接。
"""
from pathlib import Path
import sys

# 添加主项目路径到sys.path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# 从主项目导入数据库配置
from app.database import Base, engine, SessionLocal, get_db

__all__ = ["Base", "engine", "SessionLocal", "get_db"]
```

#### `admin/app/middleware.py`
```python
"""
管理后台中间件
"""
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse


class AdminAuthMiddleware(BaseHTTPMiddleware):
    """
    管理后台认证中间件

    检查用户是否已登录，未登录则重定向到登录页。
    """

    async def dispatch(self, request: Request, call_next):
        # TODO: 在用户管理模块中实现
        # 公开路径（无需认证）
        public_paths = ["/login", "/health", "/static"]

        # 检查是否是公开路径
        is_public = any(
            request.url.path.startswith(path)
            for path in public_paths
        )

        if not is_public:
            # 检查session中是否有用户信息
            user_id = request.session.get("admin_user_id")
            if not user_id:
                # 未登录，重定向到登录页
                return RedirectResponse(url="/login", status_code=302)

        response = await call_next(request)
        return response
```

#### `admin/app/dependencies.py`
```python
"""
管理后台依赖注入
"""
from typing import Optional
from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from .database import get_db


async def get_current_admin_user(request: Request):
    """
    获取当前登录的管理员

    TODO: 在用户管理模块中实现
    """
    return None


async def require_admin(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    要求用户必须是管理员

    TODO: 在用户管理模块中实现
    """
    pass
```

#### `admin/app/utils.py`
```python
"""
管理后台工具函数
"""
from typing import Any, Dict
from datetime import datetime


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
    return {
        "success": True,
        "message": message,
        "data": data
    }


def error_response(message: str = "操作失败", code: int = 400) -> Dict:
    """
    错误响应格式

    Args:
        message: 错误信息
        code: 错误代码

    Returns:
        标准响应字典
    """
    return {
        "success": False,
        "message": message,
        "code": code
    }
```

### Step 5: 创建测试配置

#### `admin/tests/conftest.py`
```python
"""
管理后台测试配置
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from admin.app.database import Base
from admin.app.main import app


@pytest.fixture(scope="session")
def test_db():
    """创建测试数据库"""
    engine = create_engine("sqlite:///./test_admin.db")
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(test_db):
    """创建数据库会话"""
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_db
    )
    session = TestingSessionLocal()
    yield session
    session.close()


@pytest.fixture(scope="module")
def client():
    """创建测试客户端"""
    return TestClient(app)
```

### Step 6: 创建配置文件

#### `admin/.gitignore`
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# 虚拟环境
venv/
ENV/

# 测试
.pytest_cache/
.coverage
htmlcov/
test_admin.db

# 上传文件
uploads/*
!uploads/.gitkeep

# IDE
.vscode/
.idea/
*.swp
*.swo

# 环境变量
.env
```

#### `admin/README.md`
```markdown
# 博文教育管理后台

独立的FastAPI管理后台应用。

## 目录结构

\`\`\`
admin/
├── app/          # 应用代码
├── templates/    # 模板文件
├── static/       # 静态资源
├── tests/        # 测试文件
└── uploads/      # 上传文件
\`\`\`

## 快速开始

\`\`\`bash
# 进入admin目录
cd admin

# 运行应用（从项目根目录）
uvicorn admin.app.main:app --reload --port 8001

# 运行测试
pytest tests/ -v
\`\`\`

## 访问地址

- 管理后台: http://localhost:8001
- API文档: http://localhost:8001/docs
\`\`\`
```

### Step 7: 创建占位模板文件

详见TASK.md中的模板文件内容。

### Step 8: 创建基础静态资源

详见TASK.md中的CSS和JS内容。

### Step 9: 运行测试验证 (Green)

```bash
# 运行所有测试
pytest admin/tests/test_infrastructure.py -v

# 验证17个测试全部通过
# 查看覆盖率
pytest admin/tests/ --cov=admin/app --cov-report=html
```

### Step 10: 代码质量检查 (Refactor)

```bash
# 格式化代码
black admin/app/
isort admin/app/

# 类型检查
mypy admin/app/

# 代码检查
ruff check admin/app/
```

---

## ✅ 完成标准

### 目录结构
- [ ] admin/ 根目录存在
- [ ] admin/app/ 目录存在
- [ ] admin/templates/ 目录存在
- [ ] admin/static/ 目录存在
- [ ] admin/tests/ 目录存在
- [ ] admin/uploads/ 目录存在

### 应用文件
- [ ] admin/app/main.py 存在且可运行
- [ ] admin/app/config.py 存在
- [ ] admin/app/database.py 存在
- [ ] admin/app/middleware.py 存在
- [ ] admin/app/dependencies.py 存在
- [ ] admin/app/utils.py 存在

### 测试文件
- [ ] admin/tests/test_infrastructure.py 存在
- [ ] admin/tests/conftest.py 存在
- [ ] pytest.ini 存在（项目根目录）

### 测试结果
- [ ] 17 个测试全部通过
- [ ] 测试覆盖率 ≥ 90%

### 代码质量
- [ ] Black 格式化通过
- [ ] isort 排序通过
- [ ] mypy 类型检查通过
- [ ] ruff 代码检查通过

### 应用可运行
- [ ] 可以启动后台应用: `uvicorn admin.app.main:app --reload --port 8001`
- [ ] 访问 http://localhost:8001 返回正常
- [ ] 访问 http://localhost:8001/health 返回 {"status": "ok"}
- [ ] 访问 http://localhost:8001/docs 显示API文档

---

## 📊 验证命令

```bash
# 1. 验证目录结构
ls -la admin/
ls -la admin/app/
ls -la admin/templates/
ls -la admin/static/
ls -la admin/tests/

# 2. 验证依赖安装
pip list | grep bcrypt
pip list | grep Pillow
pip list | grep mistune
pip list | grep pytest

# 3. 运行测试
pytest admin/tests/test_infrastructure.py -v

# 4. 查看覆盖率
pytest admin/tests/ --cov=admin/app --cov-report=term-missing

# 5. 代码质量检查
black admin/app/ --check
isort admin/app/ --check
mypy admin/app/
ruff check admin/app/

# 6. 启动应用
uvicorn admin.app.main:app --reload --port 8001

# 7. 测试API
curl http://localhost:8001/
curl http://localhost:8001/health
```

---

## 🔄 交付物

1. ✅ 完整的admin独立目录结构
2. ✅ 可运行的后台应用入口
3. ✅ 基础Python文件（带文档字符串）
4. ✅ pytest配置文件
5. ✅ requirements.txt（已更新）
6. ✅ 17个通过的测试用例
7. ✅ README.md说明文档
8. ✅ .gitignore配置

---

## 📝 注意事项

1. **完全独立**: admin/目录应该完全独立，不依赖主项目结构
2. **数据库共享**: 通过admin/app/database.py引用主项目的数据库
3. **独立运行**: 可以单独启动admin应用（端口8001）
4. **Git提交**: 完成后提交到Git

---

## 🔗 相关文档

- [admin-system-design.md](../../admin-system-design.md) - 系统设计文档
- [admin-development-plan.md](../../admin-development-plan.md) - 总体开发计划
- [TODO.md](./TODO.md) - 本模块待办事项
