# 模块 01: 基础设施搭建

**模块编号**: 01
**模块名称**: Infrastructure Setup
**优先级**: P0 (最高)
**预计工时**: 2 天
**负责 Subagent**: infrastructure-setup
**依赖**: 无

---

## 📋 任务概述

搭建管理后台系统的基础架构，包括目录结构、依赖配置、测试环境等。这是整个管理后台开发的基石。

---

## 🎯 任务目标

1. ✅ 创建规范的项目目录结构
2. ✅ 配置所有必需的依赖包
3. ✅ 建立完整的测试环境
4. ✅ 创建基础模板和静态资源框架

---

## 📁 目录结构设计

需要创建以下目录结构：

```
app/admin/
├── __init__.py                 # 管理后台包初始化
├── routers/                    # 路由模块目录
│   └── __init__.py
├── middleware.py               # 认证中间件
├── dependencies.py             # 依赖注入
└── utils.py                    # 工具函数

templates/admin/
├── base.html                   # 基础布局模板
├── login.html                  # 登录页面（占位）
├── dashboard.html              # 仪表板（占位）
└── components/                 # 公共组件
    ├── header.html
    ├── sidebar.html
    └── pagination.html

static/admin/
├── css/
│   └── admin.css              # 管理后台样式
├── js/
│   └── admin.js               # 管理后台脚本
└── images/                    # 后台用图片

tests/admin/
├── __init__.py
├── conftest.py                # pytest 配置
└── test_infrastructure.py     # 基础设施测试
```

---

## 📦 依赖包清单

### 新增依赖（需要添加到 requirements.txt）

```txt
# 密码加密
bcrypt==4.1.2

# Session 管理
itsdangerous==2.1.2

# 图片处理
Pillow==10.2.0

# Markdown 处理
mistune==3.0.2

# 测试框架
pytest==8.0.0
pytest-asyncio==0.23.0
pytest-cov==4.1.0
httpx==0.26.0

# 代码质量
ruff==0.1.11
```

### 已有依赖（确认存在）

- fastapi==0.109.0
- uvicorn[standard]==0.27.0
- sqlalchemy==2.0.25
- jinja2==3.1.3
- python-slugify==8.0.3
- black==24.1.1
- isort==5.13.2
- mypy==1.8.0

---

## 🧪 测试环境配置

### pytest 配置文件

创建 `pytest.ini`:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --strict-markers
    --cov=app/admin
    --cov-report=html
    --cov-report=term-missing
markers =
    unit: 单元测试
    integration: 集成测试
    slow: 慢速测试
asyncio_mode = auto
```

### conftest.py 配置

创建 `tests/admin/conftest.py`:

```python
"""
管理后台测试配置
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.main import app


@pytest.fixture(scope="session")
def test_db():
    """创建测试数据库"""
    engine = create_engine("sqlite:///./test.db")
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

---

## ✅ TDD 测试用例

### 测试文件: `tests/admin/test_infrastructure.py`

需要编写以下测试用例：

```python
"""
基础设施测试
"""
import os
import pytest
from pathlib import Path


class TestDirectoryStructure:
    """测试目录结构"""

    def test_admin_directory_exists(self):
        """测试 app/admin 目录存在"""
        assert Path("app/admin").exists()
        assert Path("app/admin").is_dir()

    def test_admin_routers_directory_exists(self):
        """测试 app/admin/routers 目录存在"""
        assert Path("app/admin/routers").exists()

    def test_admin_templates_directory_exists(self):
        """测试 templates/admin 目录存在"""
        assert Path("templates/admin").exists()

    def test_admin_static_directory_exists(self):
        """测试 static/admin 目录存在"""
        assert Path("static/admin").exists()

    def test_tests_admin_directory_exists(self):
        """测试 tests/admin 目录存在"""
        assert Path("tests/admin").exists()


class TestDependencies:
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


class TestPytestConfiguration:
    """测试 pytest 配置"""

    def test_pytest_ini_exists(self):
        """测试 pytest.ini 存在"""
        assert Path("pytest.ini").exists()

    def test_conftest_exists(self):
        """测试 conftest.py 存在"""
        assert Path("tests/admin/conftest.py").exists()


class TestBaseFiles:
    """测试基础文件"""

    def test_admin_init_exists(self):
        """测试 app/admin/__init__.py 存在"""
        assert Path("app/admin/__init__.py").exists()

    def test_admin_middleware_exists(self):
        """测试 middleware.py 存在"""
        assert Path("app/admin/middleware.py").exists()

    def test_admin_dependencies_exists(self):
        """测试 dependencies.py 存在"""
        assert Path("app/admin/dependencies.py").exists()

    def test_admin_utils_exists(self):
        """测试 utils.py 存在"""
        assert Path("app/admin/utils.py").exists()
```

**测试统计**:
- 测试类: 4 个
- 测试用例: 15 个
- 预期全部通过

---

## 📝 开发步骤（TDD）

### Step 1: 编写测试 (Red)

```bash
# 创建测试文件
touch tests/admin/test_infrastructure.py

# 编写上述所有测试用例
# 运行测试（预期失败）
pytest tests/admin/test_infrastructure.py -v
```

### Step 2: 创建目录结构 (Green)

```bash
# 创建 app/admin 目录
mkdir -p app/admin/routers

# 创建模板目录
mkdir -p templates/admin/components

# 创建静态资源目录
mkdir -p static/admin/{css,js,images}

# 创建测试目录
mkdir -p tests/admin
```

### Step 3: 创建基础文件

```bash
# 创建 Python 包文件
touch app/admin/__init__.py
touch app/admin/routers/__init__.py
touch app/admin/middleware.py
touch app/admin/dependencies.py
touch app/admin/utils.py

# 创建测试配置
touch tests/admin/__init__.py
touch tests/admin/conftest.py
```

### Step 4: 更新 requirements.txt

```bash
# 编辑 requirements.txt 添加新依赖
```

### Step 5: 安装依赖

```bash
# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### Step 6: 创建 pytest 配置

```bash
# 创建 pytest.ini
touch pytest.ini
```

### Step 7: 运行测试验证 (Green)

```bash
# 再次运行测试（预期全部通过）
pytest tests/admin/test_infrastructure.py -v

# 查看覆盖率
pytest tests/admin/test_infrastructure.py --cov=app/admin --cov-report=html
```

---

## 📄 基础文件内容

### `app/admin/__init__.py`

```python
"""
博文教育管理后台

这是管理后台的主包，包含所有管理功能模块。
"""

__version__ = "1.0.0"
__author__ = "maxazure"
```

### `app/admin/middleware.py`

```python
"""
管理后台中间件

包含认证中间件等。
"""

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class AdminAuthMiddleware(BaseHTTPMiddleware):
    """
    管理后台认证中间件

    检查用户是否已登录，未登录则重定向到登录页。
    """

    async def dispatch(self, request: Request, call_next):
        # TODO: 在用户管理模块中实现
        response = await call_next(request)
        return response
```

### `app/admin/dependencies.py`

```python
"""
管理后台依赖注入

提供常用的依赖项。
"""

from typing import Optional
from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database import get_db


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

### `app/admin/utils.py`

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

---

## ✅ 完成标准

### 功能性要求

- [x] 所有目录创建完成
- [x] 所有基础文件创建完成
- [x] 所有依赖包安装成功
- [x] pytest 配置正确
- [x] 所有测试通过 (15/15)

### 质量要求

- [x] 代码符合 PEP 8 规范
- [x] 所有函数有类型提示
- [x] 所有函数有文档字符串
- [x] 测试覆盖率 = 100%

### 文档要求

- [x] 更新 TODO.md 记录完成情况
- [x] 所有代码有清晰注释

---

## 📊 验证命令

```bash
# 1. 验证目录结构
ls -la app/admin/
ls -la templates/admin/
ls -la static/admin/
ls -la tests/admin/

# 2. 验证依赖安装
pip list | grep bcrypt
pip list | grep Pillow
pip list | grep mistune
pip list | grep pytest

# 3. 运行测试
pytest tests/admin/test_infrastructure.py -v

# 4. 查看覆盖率
pytest tests/admin/test_infrastructure.py --cov=app/admin --cov-report=term-missing

# 5. 代码质量检查
black app/admin/ --check
isort app/admin/ --check
mypy app/admin/
```

---

## 🔄 交付物

1. ✅ 完整的目录结构
2. ✅ 基础 Python 文件（带文档字符串）
3. ✅ pytest 配置文件
4. ✅ requirements.txt（已更新）
5. ✅ 15 个通过的测试用例
6. ✅ 更新的 TODO.md

---

## 📝 注意事项

1. **虚拟环境**: 确保在虚拟环境中安装依赖
2. **文件权限**: 确保所有文件有正确的权限
3. **Git 提交**: 完成后提交代码到 Git
4. **文档更新**: 完成后更新模块的 TODO.md

---

## 🔗 相关文档

- [admin-system-design.md](../../admin-system-design.md) - 系统设计文档
- [admin-development-plan.md](../../admin-development-plan.md) - 总体开发计划
- [TODO.md](./TODO.md) - 本模块待办事项
