# TODO - 模块 02: 用户管理

**模块**: User Management  
**开始时间**: 待定  
**完成时间**: 待定  
**负责人**: user-management-tdd subagent

---

## 🔄 进行中

暂无

---

## ✅ 已完成

暂无

---

## 📋 待办事项

### Phase 1: 编写测试 (TDD - Red)

- [ ] 创建测试文件 `tests/admin/test_auth.py`
- [ ] 编写管理员模型测试类 `TestAdminUserModel` (5个测试)
  - [ ] test_create_admin_user
  - [ ] test_password_hashing
  - [ ] test_password_verification
  - [ ] test_username_unique
  - [ ] test_email_unique
- [ ] 编写登录登出测试类 `TestLoginLogout` (5个测试)
  - [ ] test_login_page_loads
  - [ ] test_login_with_valid_credentials
  - [ ] test_login_with_invalid_username
  - [ ] test_login_with_invalid_password
  - [ ] test_logout
- [ ] 编写认证中间件测试类 `TestAuthMiddleware` (3个测试)
  - [ ] test_admin_pages_require_login
  - [ ] test_login_page_accessible_without_auth
  - [ ] test_authenticated_user_can_access_admin
- [ ] 编写密码修改测试类 `TestPasswordChange` (4个测试)
  - [ ] test_change_password_page_loads
  - [ ] test_change_password_with_correct_old_password
  - [ ] test_change_password_with_wrong_old_password
  - [ ] test_change_password_with_mismatched_confirmation
- [ ] 编写 Session 管理测试类 `TestSessionManagement` (3个测试)
  - [ ] test_session_created_on_login
  - [ ] test_session_cleared_on_logout
  - [ ] test_last_login_time_updated
- [ ] 运行测试验证失败 `pytest tests/admin/test_auth.py -v`

### Phase 2: 创建数据模型 (TDD - Green)

- [ ] 创建 `app/models/admin_user.py`
- [ ] 定义 AdminUser 类(继承 Base)
- [ ] 添加字段: id, username, password_hash, email, last_login_at, created_at, updated_at
- [ ] 实现 `set_password()` 方法(使用 bcrypt)
- [ ] 实现 `verify_password()` 方法
- [ ] 添加 `__repr__()` 方法

### Phase 3: 创建数据库迁移

- [ ] 生成迁移文件 `alembic revision --autogenerate -m "add admin_users table"`
- [ ] 检查迁移文件内容
- [ ] 执行迁移 `alembic upgrade head`
- [ ] 验证表创建成功

### Phase 4: 实现登录路由 (TDD - Green)

- [ ] 创建 `app/admin/routers/auth.py`
- [ ] 实现 `GET /admin/login` (登录页面)
- [ ] 实现 `POST /admin/login` (登录处理)
  - [ ] 查询用户
  - [ ] 验证密码
  - [ ] 更新 last_login_at
  - [ ] 创建 session
  - [ ] 重定向到仪表板
- [ ] 实现 `GET /admin/logout` (登出)
  - [ ] 清除 session
  - [ ] 重定向到登录页

### Phase 5: 实现 Session 管理

- [ ] 在 `main.py` 添加 SessionMiddleware
- [ ] 配置 SECRET_KEY (从环境变量读取)
- [ ] 设置 Cookie 参数(HTTPOnly, SameSite)
- [ ] 测试 Session 创建和销毁

### Phase 6: 实现认证中间件 (TDD - Green)

- [ ] 编辑 `app/admin/middleware.py`
- [ ] 实现 AdminAuthMiddleware 类
- [ ] 定义公开路径列表
- [ ] 检查 session 中的 admin_user_id
- [ ] 未登录用户重定向到登录页
- [ ] 在 main.py 注册中间件

### Phase 7: 实现密码修改功能

- [ ] 在 `app/admin/routers/auth.py` 添加路由
- [ ] 实现 `GET /admin/profile/change-password` (页面)
- [ ] 实现 `POST /admin/profile/change-password` (处理)
  - [ ] 验证旧密码
  - [ ] 验证新密码一致性
  - [ ] 更新密码
  - [ ] 重定向并显示成功消息

### Phase 8: 创建模板文件

- [ ] 创建 `templates/admin/login.html`
  - [ ] Bootstrap 5 样式
  - [ ] 表单: username, password
  - [ ] 错误消息显示
  - [ ] 响应式设计
- [ ] 创建 `templates/admin/profile/change-password.html`
  - [ ] 继承 base.html
  - [ ] 表单: old_password, new_password, confirm_password
  - [ ] 错误消息和成功消息显示

### Phase 9: 创建初始化脚本

- [ ] 创建 `scripts/init_admin.py`
- [ ] 实现 init_admin() 函数
  - [ ] 检查管理员是否存在
  - [ ] 创建默认管理员(username: admin)
  - [ ] 设置默认密码(admin123)
  - [ ] 显示创建成功消息和安全提示
- [ ] 运行脚本创建管理员 `python scripts/init_admin.py`

### Phase 10: 运行测试验证 (TDD - Green)

- [ ] 运行所有测试 `pytest tests/admin/test_auth.py -v`
- [ ] 验证 22 个测试全部通过
- [ ] 查看测试覆盖率 `pytest tests/admin/test_auth.py --cov=app/admin --cov=app/models --cov-report=html`
- [ ] 确认覆盖率 >= 90%

### Phase 11: 代码质量检查 (TDD - Refactor)

- [ ] 运行 Black 格式化 `black app/admin/ app/models/`
- [ ] 运行 isort 排序 `isort app/admin/ app/models/`
- [ ] 运行 mypy 类型检查 `mypy app/admin/ app/models/`
- [ ] 运行 ruff 代码检查 `ruff check app/admin/ app/models/`
- [ ] 修复所有警告和错误

### Phase 12: 手动测试

- [ ] 启动服务器 `uvicorn main:app --reload`
- [ ] 测试登录页面访问
- [ ] 测试正确凭据登录
- [ ] 测试错误凭据登录
- [ ] 测试未授权访问重定向
- [ ] 测试登出功能
- [ ] 测试密码修改功能

### Phase 13: 文档与提交

- [ ] 更新本 TODO.md 标记完成任务
- [ ] 创建 Git commit 提交代码
  - 提交信息: "feat: 实现管理后台用户认证系统"
- [ ] 验证所有文件已提交

---

## 📊 任务统计

- **总任务数**: 70+
- **已完成**: 0
- **进行中**: 0
- **待办**: 70+
- **完成率**: 0%

---

## ✅ 完成标准检查清单

### 数据模型
- [ ] AdminUser 模型创建完成
- [ ] 所有字段定义正确
- [ ] set_password() 方法正常工作
- [ ] verify_password() 方法正常工作
- [ ] 数据库迁移成功

### 登录功能
- [ ] 登录页面可访问
- [ ] 正确凭据可以登录
- [ ] 错误凭据登录失败并显示错误
- [ ] 登录后创建 session
- [ ] 登录后重定向到仪表板

### 登出功能
- [ ] 登出清除 session
- [ ] 登出后重定向到登录页
- [ ] 登出后不能访问管理页面

### 认证中间件
- [ ] 未登录访问管理页面重定向
- [ ] 已登录可以访问管理页面
- [ ] 登录页面无需认证
- [ ] 静态资源无需认证

### 密码修改
- [ ] 密码修改页面需要登录
- [ ] 正确旧密码可以修改
- [ ] 错误旧密码不能修改
- [ ] 新密码不一致不能修改
- [ ] 修改后新密码生效

### 测试覆盖
- [ ] 22 个测试全部通过
- [ ] 测试覆盖率 >= 90%
- [ ] 无失败的测试

### 代码质量
- [ ] Black 格式化通过
- [ ] isort 排序通过
- [ ] mypy 类型检查通过
- [ ] ruff 代码检查通过
- [ ] 无代码质量警告

---

## 📝 备注

- 所有任务必须按照 TDD 流程执行: Red → Green → Refactor
- 每完成一个 Phase，立即更新此 TODO.md
- 遇到问题记录在下方"问题与解决"部分
- 密码必须使用 bcrypt 加密
- Session 必须使用环境变量配置 SECRET_KEY

---

## ❓ 问题与解决

暂无

---

**最后更新**: 2025-11-13  
**状态**: 待开始
