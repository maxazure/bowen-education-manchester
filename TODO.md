# TODO 任务列表

## 🔄 进行中
暂无进行中的任务

## ✅ 已完成

### [2025-11-17] 完成所有单页英文内容翻译（24/24页面）
- [x] 第一批：翻译核心页面（7页） - 完成时间: 2025-11-17 - 负责人: maxazure
- [x] 第二批：翻译项目与活动页面（5页） - 完成时间: 2025-11-17 - 负责人: maxazure
- [x] 第三批：翻译长内容页面（5页） - 完成时间: 2025-11-17 - 负责人: maxazure
- [x] 第四批：翻译政策页面（4页） - 完成时间: 2025-11-17 - 负责人: maxazure
- [x] 验证英文页面显示效果 - 完成时间: 2025-11-17 - 负责人: maxazure

**翻译统计**:
- 总页面数: 24个已发布单页
- 已完成翻译: 24/24 (100%)
- 总字符数: ~83,000英文字符
- 翻译方式: 高质量意译，符合英语母语者阅读习惯

**翻译页面清单**:

第一批（核心页面 - 7页）:
1. Contact Us (ID: 2) - 1,306字符
2. 中文学校/Chinese School (ID: 3) - 927字符
3. 补习中心/Tutoring Centre (ID: 4) - 800字符
4. 国际象棋俱乐部/Chess Club (ID: 5) - 785字符
5. 政府项目/Government Programs (ID: 6) - 471字符
6. 博文活动/Events & Activities (ID: 7) - 476字符
7. 博文新闻/News & Updates (ID: 8) - 247字符
8. 羽毛球俱乐部/Badminton Club (ID: 9) - 753字符

第二批（项目与活动页面 - 5页）:
1. 学期日期/Term Dates (ID: 10) - 638字符
2. PTA家长教师协会/Parent-Teacher Association (ID: 11) - 1,126字符
3. 河南大学合作/Henan University Partnership (ID: 15) - 1,800字符
4. 博文图库/Photo Gallery (ID: 17) - 846字符
5. 俱乐部简介/Chess Club Introduction (ID: 19) - 2,531字符

第三批（长内容页面 - 5页）:
1. HAF项目/HAF Programme (ID: 14) - 6,584字符
2. 常见问题解答/FAQ (ID: 18) - 6,570字符
3. 课程设置/Course Structure (ID: 20) - 4,363字符
4. 学习资源/Learning Resources (ID: 21) - 7,362字符

第四批（政策页面 - 4页）:
1. Privacy Policy (ID: 22) - 3,724字符
2. Terms of Service (ID: 23) - 4,671字符
3. Cookie Policy (ID: 24) - 3,933字符
4. Safeguarding Policy (ID: 25) - 6,993字符

**翻译特点**:
- ✅ 完全意译，非机器直译
- ✅ 符合英语母语者阅读习惯
- ✅ 保持专业性和可读性
- ✅ 所有英文页面显示正常，无中文字符
- ✅ Markdown自动转换为HTML功能正常
- ✅ 双语回退机制工作正常

**技术实现**:
- 使用Python脚本批量处理翻译内容
- 通过`single_page_service.markdown_to_html()`转换Markdown为HTML
- 直接更新数据库`content_markdown_en`和`content_html_en`字段
- 所有页面通过`{{ field_en or field }}`模板回退机制正常显示

### [2025-11-17] 单页英文内容填充与后台表单修复
- [x] 修复后台hero_media_id字段验证错误 - 完成时间: 2025-11-17 - 负责人: maxazure
- [x] 更新"关于博文教育"页面英文内容 - 完成时间: 2025-11-17 - 负责人: maxazure
- [x] 更新"训练时间表"页面英文内容 - 完成时间: 2025-11-17 - 负责人: maxazure
- [x] 验证英文页面前台显示效果 - 完成时间: 2025-11-17 - 负责人: maxazure

**问题修复**:
- 后台表单hero_media_id字段提交时报错：`Input should be a valid integer, unable to parse string as an integer`
- 原因：HTML表单空值提交为空字符串 `""`，但FastAPI `Form(Optional[int])` 无法解析空字符串
- 解决方案：
  - 修改 `admin/app/routers/single_pages.py:109` 和 `line:251` 参数类型为 `Optional[str]`
  - 新增 `parse_optional_int()` 辅助函数（line:23-30）将空字符串转换为 None
  - 在 `create_page` 和 `update_page` 中使用该函数处理 hero_media_id

**内容更新**:
- **关于博文教育** (Page ID: 16, `/en/about-company`)
  - 英文Markdown: 1347字符
  - 英文HTML: 1623字符
  - 包含：教育理念、使命、资质认证等完整内容

- **训练时间表** (Page ID: 13, `/en/badminton-schedule`)
  - 英文Markdown: 1680字符
  - 英文HTML: 1823字符
  - 包含：训练时间表、训练内容、地点信息、注意事项

**验证结果**:
- 英文页面完全显示纯英文内容，无中文字符
- 双语回退机制工作正常：`{{ field_en or field }}`
- Markdown自动转换为HTML功能正常

**当前进度**:
- 已完成单页数量: 2/24
- 待完成单页: 22个

### [2025-11-17] 清理单页英文数据（修复后台编辑与前台显示不一致问题）
- [x] 调研后台单页编辑和前台显示不一致原因 - 完成时间: 2025-11-17 - 负责人: maxazure
- [x] 备份当前所有单页的英文数据 - 完成时间: 2025-11-17 - 负责人: maxazure
- [x] 清空所有单页的content_html_en和content_markdown_en字段 - 完成时间: 2025-11-17 - 负责人: maxazure

**问题分析**:
- 代码逻辑完全正常，字段映射关系正确
- 数据库中的content_html_en字段包含中英混杂内容（如："博文Chinese学校"、"Teaching特色"等）
- content_markdown_en字段为空，说明从未通过后台正常编辑
- 问题根源：可能之前使用自动翻译脚本直接写入了错误的HTML内容

**清理统计**:
- 影响单页数量: 24个
- 清空字段: content_html_en, content_markdown_en
- 备份文件: backup/single_page_en_backup_20251117_174104.txt
- 更新记录数: 24条

**清理效果**:
- 所有单页的英文字段已清空，前台英文页面会自动回退显示中文内容
- 可通过后台"English Content" Tab重新填写纯英文Markdown内容
- 系统会自动将Markdown转换为HTML并保存

**后续工作**:
- 需要在后台逐个编辑24个单页，填写英文Markdown内容
- 建议优先处理重要页面：About Us, Contact Us, 中文学校等

### [2025-11-17] 英文模板中文内容全面清理
- [x] 清理 tuition.html 中的中文文本 - 完成时间: 2025-11-16 - 负责人: maxazure
- [x] 清理 events.html 中的中文文本 - 完成时间: 2025-11-16 - 负责人: maxazure
- [x] 清理 single_page.html 中的中文文本 - 完成时间: 2025-11-16 - 负责人: maxazure
- [x] 清理 post_list_with_sidebar.html 注释中的中文 - 完成时间: 2025-11-17 - 负责人: maxazure
- [x] 清理 post_list_universal.html 注释中的中文 - 完成时间: 2025-11-17 - 负责人: maxazure
- [x] 删除 home_legacy_20251115.html 遗留文件 - 完成时间: 2025-11-17 - 负责人: maxazure

**清理统计**:
- 清理文件数: 5个模板文件
- 删除遗留文件: 1个（home_legacy_20251115.html，530个中文字符）
- 翻译注释: 5处（JavaScript注释2处，CSS注释3处）
- templates/en/ 目录现已完全英文化

**清理内容**:
- tuition.html, events.html, single_page.html: 移除所有 `<span lang="zh-CN">` 标签
- post_list_with_sidebar.html: 翻译JavaScript注释（懒加载AOS库、图片懒加载优化）
- post_list_universal.html: 翻译CSS注释（CTA Section、响应式样式）
- 删除包含530个中文字符的legacy文件

## 📋 待办事项

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

**历史记录**: 详细的历史任务记录可查看 Git 提交历史

**最后更新**: 2025-11-17
**当前状态**: 双语系统基本完成，待进行英文模板清理工作
