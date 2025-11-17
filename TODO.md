# TODO 任务列表

## 🔄 进行中
暂无进行中的任务

## ✅ 已完成

### [2025-11-17] 英文页面中文内容系统性清理
- [x] 生成英文页面中文内容审计报告 - 完成时间: 2025-11-17 - 负责人: maxazure
- [x] 修复 Priority 1 问题(Hero区块、页面标题) - 完成时间: 2025-11-17 - 负责人: maxazure
- [x] 修复 Priority 2 问题(Meta Description) - 完成时间: 2025-11-17 - 负责人: maxazure
- [x] 修复 Priority 3 问题(课程标题、图片alt标签) - 完成时间: 2025-11-17 - 负责人: maxazure

**修复内容**:
- 修复2个栏目的Hero区块中文显示(badminton-gallery, programmes-parks)
- 修复4个页面的<title>标签中文(news, chess-events, chess-news, badminton-events)
- 修复6个页面的Meta Description中文(about-company, chess-about, chess-courses, chess-resources, events-henan, programmes-haf)
- 修复7个课程的英文标题(Foundation/Primary Mandarin, GCSE/A-Level Chinese, HSK, Cantonese)
- 修复school-curriculum页面图片alt标签中文问题

**涉及文件**:
- templates/en/components/hero_standard.html - Hero逻辑优化
- templates/en/post_list_with_sidebar.html - 标题和图片alt修复
- templates/en/post_list_universal.html - 标题和meta修复
- templates/en/gallery.html - 标题和meta修复
- instance/database.db - 数据库英文字段更新

**技术要点**:
- 使用Jinja2的`column_name`自定义过滤器实现i18n
- 数据库字段优先级: hero_title_en > name_en > name
- 模板变量回退逻辑: title_en or title

### [2025-11-17] 更新博文教育简介文字
- [x] 翻译新的中文简介为英文 - 完成时间: 2025-11-17 - 负责人: maxazure
- [x] 修改中文首页(templates/zh/home.html)简介区块 - 完成时间: 2025-11-17 - 负责人: maxazure
- [x] 修改英文首页(templates/en/home.html)简介区块 - 完成时间: 2025-11-17 - 负责人: maxazure
- [x] 修改中文关于页面(templates/zh/about.html)简介区块 - 完成时间: 2025-11-17 - 负责人: maxazure
- [x] 修改英文关于页面(templates/en/about.html)简介区块 - 完成时间: 2025-11-17 - 负责人: maxazure

**更新内容**:
- 标语更新为: "立足英国 · 服务社区 · 传承文化 · 联通中外"
- 新增机构资质说明: Ofsted注册认证、Tax-Free Childcare政府育儿补贴资质
- 强调教育理念: "Learn · Share · Bridge(学习 · 分享 · 桥梁)"
- 新增使命愿景段落: 将中文教育融入英国主流教育体系,塑造孩子的精神世界
- 涉及文件:
  - templates/zh/home.html (第827-833行)
  - templates/en/home.html (第825-831行)
  - templates/zh/about.html (第17-42行)
  - templates/en/about.html (第17-41行)

### [2025-11-16] 产品和活动双语支持、品牌名称统一
- [x] Product 模型双语支持 - 完成时间: 2025-11-16 - 负责人: maxazure
- [x] Event 模型双语支持 - 完成时间: 2025-11-16 - 负责人: maxazure
- [x] 产品管理后台 Tab 双语编辑界面 - 完成时间: 2025-11-16 - 负责人: maxazure
- [x] 产品前台英文模板回退逻辑 - 完成时间: 2025-11-16 - 负责人: maxazure
- [x] 品牌名称统一更新为"博文教育集团" - 完成时间: 2025-11-16 - 负责人: maxazure
- [x] README 文档更新 - 完成时间: 2025-11-16 - 负责人: maxazure

**技术要点**:
- 数据库新增 13 个英文字段（ProductCategory 1个, Product 6个, Event 6个）
- Bootstrap 5 Tab 实现中英文分离编辑界面
- Jinja2 `or` 操作符实现英文优先回退逻辑
- 全站品牌名称统一更新（7个文件, 9处）

### [2025-11-16] 英文模板文件中文文本清理（部分完成）
- [x] 清理 school.html - 完成时间: 2025-11-16 - 负责人: maxazure
- [x] 清理 contact.html - 完成时间: 2025-11-16 - 负责人: maxazure
- [x] 清理 programmes.html - 完成时间: 2025-11-16 - 负责人: maxazure
- [x] 清理 layout_page.html - 完成时间: 2025-11-16 - 负责人: maxazure

## 📋 待办事项

### 英文模板中文清理（高优先级）
- [ ] 清理 tuition.html 中的中文文本(96处) - 优先级: 高 - 预计工时: 2h
- [ ] 清理 events.html 中的中文文本(75处) - 优先级: 高 - 预计工时: 1.5h
- [ ] 清理 single_page.html 中的中文文本(33处) - 优先级: 中 - 预计工时: 1h
- [ ] 清理其他模板文件中的中文文本 - 优先级: 中 - 预计工时: 2h

**清理规则**:
1. 移除所有 `<span lang="zh-CN">中文文本</span>` 及其中文内容
2. 保留 `<span lang="en-GB">英文文本</span>` 的内容但移除lang属性
3. 将中文标题、标签、按钮文本替换为英文
4. 更新所有内部链接URL，添加 `/en/` 前缀

### 系统优化
- [ ] 优化数据库查询性能 - 优先级: 中 - 预计工时: 4h
- [ ] 添加缓存机制 - 优先级: 中 - 预计工时: 3h
- [ ] 完善 SEO 配置 - 优先级: 低 - 预计工时: 2h

## 🐛 已知问题
暂无已知问题

## 💡 优化建议
- [ ] 考虑使用 i18n 框架替代当前的双语实现 - 提出时间: 2025-11-16 - 预期收益: 更好的可维护性
- [ ] 添加自动化测试覆盖 - 提出时间: 2025-11-16 - 预期收益: 提高代码质量
- [ ] 实施 CI/CD 流程 - 提出时间: 2025-11-16 - 预期收益: 自动化部署

## 📚 学习笔记

### 双语支持最佳实践
- **字段命名规范**: 英文字段统一使用 `_en` 后缀
- **回退逻辑**: 使用 Jinja2 的 `or` 操作符实现优雅的回退: `{{ field_en or field }}`
- **数据库设计**: 所有双语字段设置为 `nullable=True`，保持向后兼容
- **UI 组件**: Bootstrap Tab 可以很好地分离双语编辑区域

### Jinja2 模板技巧
- 条件渲染: `{% if parent_column.slug == 'value' %}`
- 回退逻辑: `{{ english_field or chinese_field }}`
- 安全 HTML 输出: `{{ content|safe }}`

### 数据库迁移注意事项
- 使用 `nullable=True` 确保向后兼容
- 先更新模型，再执行迁移
- 使用事务确保数据一致性

---

**历史记录**: 详细的历史任务记录已归档至 `TODO_ARCHIVE_YYYYMMDD.md` 文件

**最后更新**: 2025-11-17
**当前状态**: 双语系统基本完成，正在进行英文模板清理工作
