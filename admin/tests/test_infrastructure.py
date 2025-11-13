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
