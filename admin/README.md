# 博文教育管理后台

独立的FastAPI管理后台应用。

## 目录结构

```
admin/
├── app/          # 应用代码
├── templates/    # 模板文件
├── static/       # 静态资源
├── tests/        # 测试文件
└── uploads/      # 上传文件
```

## 快速开始

```bash
# 进入admin目录
cd admin

# 运行应用（从项目根目录）
uvicorn admin.app.main:app --reload --port 8001

# 运行测试
pytest tests/ -v
```

## 访问地址

- 管理后台: http://localhost:8001
- API文档: http://localhost:8001/docs
```
