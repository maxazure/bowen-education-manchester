# 图片生成工具使用指南

智谱 AI CogView-3-Flash 图片批量生成工具

---

## 📋 目录

- [快速开始](#快速开始)
- [配置文件格式](#配置文件格式)
- [提示词编写技巧](#提示词编写技巧)
- [使用示例](#使用示例)
- [常见问题](#常见问题)

---

## 🚀 快速开始

### 1. 环境配置

首先确保已设置 API Key：

```bash
# 临时设置（当前会话有效）
export ZHIPU_KEY="your-api-key-here"

# 永久设置（添加到 ~/.zshrc 或 ~/.bashrc）
echo 'export ZHIPU_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

### 2. 基本用法

```bash
# 使用默认配置文件 (images.json)
python3 tools/generate_images.py

# 使用自定义配置文件
python3 tools/generate_images.py --config my-images.json

# 使用绝对路径
python3 tools/generate_images.py --config /path/to/config.json
```

### 3. 查看帮助

```bash
python3 tools/generate_images.py --help
```

---

## 📝 配置文件格式

### 基本结构

配置文件使用 JSON 格式，必须包含 `output_dir` 和 `images` 两个字段：

```json
{
  "output_dir": "static/images/generated",
  "images": [
    {
      "filename": "example-image.jpg",
      "prompt": "A detailed description of the image to generate...",
      "priority": "high"
    }
  ]
}
```

### 字段说明

#### 根级别字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `output_dir` | string | ✅ | 图片保存目录（相对或绝对路径） |
| `images` | array | ✅ | 图片配置数组 |

#### 图片对象字段

| 字段 | 类型 | 必填 | 可选值 | 说明 |
|------|------|------|--------|------|
| `filename` | string | ✅ | - | 输出文件名（如 `image.jpg`） |
| `prompt` | string | ✅ | - | 英文描述提示词 |
| `priority` | string | ✅ | `high`, `medium`, `low` | 生成优先级 |

### 完整示例

```json
{
  "output_dir": "static/images/courses",
  "images": [
    {
      "filename": "chinese-classroom.jpg",
      "prompt": "A bright and modern Chinese language classroom in Manchester, UK. Young students learning Mandarin Chinese, colorful educational posters with Chinese characters on walls, professional teacher at whiteboard, warm lighting, educational atmosphere, photorealistic style",
      "priority": "high"
    },
    {
      "filename": "math-tutoring.jpg",
      "prompt": "Professional mathematics tutoring session in Manchester, UK. Student working on GCSE mathematics problems with experienced tutor, whiteboard with formulas, focused learning environment, natural daylight, photorealistic",
      "priority": "medium"
    },
    {
      "filename": "sports-activity.jpg",
      "prompt": "Children playing badminton in modern sports hall, Manchester UK, active training session with coaches, energetic atmosphere, bright indoor lighting, action photography style",
      "priority": "low"
    }
  ]
}
```

---

## ✍️ 提示词编写技巧

### 提示词结构

好的提示词应该包含以下要素：

```
[场景类型] + [主要内容] + [环境细节] + [人物描述] + [光线氛围] + [风格要求]
```

### 必须包含的要素

- ✅ **场景类型**: classroom, tutoring session, sports hall, office
- ✅ **主要内容**: learning Chinese, mathematics tutoring, badminton training
- ✅ **地点标识**: Manchester, UK（提高准确性）
- ✅ **风格要求**: photorealistic, professional photography style

### 建议包含的要素

- 📌 **年龄段**: young children (5-7), teenage students (14-16), adults
- 📌 **环境细节**: posters, whiteboard, equipment, furniture
- 📌 **光线描述**: warm lighting, natural daylight, bright indoor lighting
- 📌 **氛围营造**: educational atmosphere, energetic, focused
- 📌 **质量要求**: high quality, professional, 4K

### 避免使用

- ❌ 中文描述（API 仅支持英文）
- ❌ 过于抽象的概念（如"成功"、"希望"）
- ❌ 特定品牌名称
- ❌ 版权保护的角色或人物
- ❌ 过短的描述（少于50字符）

### 优秀提示词示例

#### 1. 中文课堂（基础班）
```
A bright and engaging Chinese language classroom in Manchester, UK.
Young students aged 5-7 learning Mandarin Chinese, colorful educational
posters with Chinese characters on walls, professional Chinese teacher
at whiteboard writing characters, young children sitting at desks with
learning materials, warm natural lighting, educational atmosphere,
professional photography style, high quality, photorealistic
```

#### 2. GCSE 数学辅导
```
Professional mathematics tutoring session in Manchester, UK. Teenage
student working on GCSE mathematics problems with experienced tutor,
whiteboard with mathematical formulas and equations, textbooks and
notebooks on desk, focused learning environment, natural daylight through
windows, modern tutoring center, professional photography style,
photorealistic
```

#### 3. 羽毛球训练
```
Professional badminton training session for children in modern sports
hall, Manchester UK. Young players aged 10-14 practicing with professional
coaches, badminton courts with nets, players holding rackets, shuttlecocks
in motion, energetic and active atmosphere, bright indoor lighting,
sports photography style, action shot, high quality
```

#### 4. 文化活动
```
Chinese cultural celebration event in community center, Manchester UK.
Children and families participating in traditional Chinese activities,
red lanterns and decorations, festive atmosphere, people wearing
traditional clothing, community gathering, warm and welcoming environment,
event photography style, photorealistic, high quality
```

#### 5. 校园环境
```
Modern educational institution building exterior in Manchester, UK.
Bright and welcoming facade with students entering, contemporary
architecture, green spaces around, sunny day with blue sky, professional
architecture photography, wide angle view, high quality
```

### 提示词优化流程

1. **初稿**: 基本场景描述
2. **补充**: 添加人物、环境、光线细节
3. **优化**: 加入地域标识和风格要求
4. **验证**: 检查是否包含所有必要要素
5. **测试**: 生成图片后根据结果调整

---

## 📖 使用示例

### 示例1: 生成课程封面图片

#### 步骤1: 创建配置文件

创建 `course-images.json`:

```json
{
  "output_dir": "static/images/courses",
  "images": [
    {
      "filename": "foundation-mandarin.jpg",
      "prompt": "A bright and engaging Chinese language classroom in Manchester, UK. Young students aged 5-7 learning Mandarin Chinese, colorful educational posters with Chinese characters on walls, professional Chinese teacher at whiteboard writing Chinese characters, young children sitting at desks with learning materials, warm natural lighting, educational atmosphere, professional photography style, high quality, photorealistic",
      "priority": "high"
    },
    {
      "filename": "gcse-chinese.jpg",
      "prompt": "A bright and engaging Chinese language classroom in Manchester, UK. Teenage students aged 14-16 learning Mandarin Chinese, colorful educational posters with Chinese characters on walls, professional Chinese teacher at whiteboard writing Chinese characters, teenage students taking notes, warm natural lighting, educational atmosphere, professional photography style, high quality, photorealistic",
      "priority": "high"
    }
  ]
}
```

#### 步骤2: 生成图片

```bash
python3 tools/generate_images.py --config course-images.json
```

#### 步骤3: 查看结果

```bash
ls -lh static/images/courses/
```

### 示例2: 生成新闻配图

#### 步骤1: 创建配置文件

创建 `news-images.json`:

```json
{
  "output_dir": "static/images/news",
  "images": [
    {
      "filename": "school-opening.jpg",
      "prompt": "School opening ceremony in Manchester, UK. Students and parents gathered in auditorium, welcoming atmosphere, banners and decorations, community event, professional event photography, photorealistic",
      "priority": "high"
    },
    {
      "filename": "exam-success.jpg",
      "prompt": "Happy teenage students celebrating exam results, Manchester UK school setting, students holding certificates, joyful expressions, natural lighting, photojournalism style, authentic moment, high quality",
      "priority": "medium"
    }
  ]
}
```

#### 步骤2: 生成图片

```bash
python3 tools/generate_images.py --config news-images.json
```

### 示例3: 批量生成多种类型图片

```bash
# 生成课程图片
python3 tools/generate_images.py --config course-images.json

# 生成活动图片
python3 tools/generate_images.py --config event-images.json

# 生成新闻图片
python3 tools/generate_images.py --config news-images.json

# 生成团队照片
python3 tools/generate_images.py --config team-images.json
```

### 示例4: 增量生成

工具会自动跳过已存在的文件，可以实现增量生成：

```bash
# 第一次运行 - 生成所有图片
python3 tools/generate_images.py --config images.json

# 修改配置文件，添加新图片
# 第二次运行 - 只生成新添加的图片
python3 tools/generate_images.py --config images.json
```

---

## 🔧 技术细节

### 图片规格

- **模型**: Zhipu AI CogView-3-Flash
- **尺寸**: 1024x1024 像素
- **格式**: JPG
- **平均大小**: 100-150 KB

### 生成流程

1. **加载配置**: 读取 JSON 配置文件
2. **验证字段**: 检查必填字段和字段值
3. **创建目录**: 自动创建输出目录（如不存在）
4. **优先级排序**: 按 high → medium → low 排序
5. **逐个生成**:
   - 检查文件是否已存在（跳过已有文件）
   - 调用 Zhipu AI API
   - 下载图片
   - 保存到指定目录
   - 显示文件大小和状态
6. **请求间隔**: 每个请求间隔 2 秒（避免限流）
7. **显示统计**: 总数、成功、失败

### API 限制

- **请求频率**: 建议 2 秒间隔（已内置）
- **并发限制**: 单线程顺序处理
- **超时时间**:
  - API 请求: 60 秒
  - 图片下载: 30 秒

---

## ❓ 常见问题

### Q1: 如何获取 API Key？

**A**: 访问 [智谱AI开放平台](https://open.bigmodel.cn/)，注册账号并创建 API Key。

### Q2: API Key 错误怎么办？

```bash
[ERROR] ZHIPU_KEY environment variable is not set!
```

**解决方法**:
```bash
# 设置环境变量
export ZHIPU_KEY="your-api-key"

# 验证设置
echo $ZHIPU_KEY
```

### Q3: 配置文件格式错误

```bash
[ERROR] Invalid JSON in 'xxx.json'
```

**解决方法**:
1. 使用 JSON 验证工具检查格式
2. 确保所有字符串用双引号 `""`
3. 检查逗号位置（最后一个元素后不要逗号）
4. 使用在线 JSON 格式化工具

### Q4: 生成的图片不符合预期

**解决方法**:
1. 优化提示词，添加更多细节
2. 增加环境、人物、光线描述
3. 明确指定风格（photorealistic, professional photography）
4. 参考本文档的优秀提示词示例

### Q5: 如何生成特定尺寸的图片？

**A**: 当前版本固定生成 1024x1024 像素的图片。如需其他尺寸，可以使用图片编辑工具后期调整。

### Q6: 可以生成动图或视频吗？

**A**: 不可以，当前工具仅支持生成静态图片（JPG 格式）。

### Q7: 生成失败如何重试？

**A**:
- 工具不会自动重试失败的图片
- 查看失败原因并修复（网络、API Key、提示词）
- 再次运行相同命令，已成功的图片会被跳过

### Q8: 如何批量删除生成的图片？

```bash
# 删除指定目录的所有图片
rm -rf static/images/courses/*.jpg

# 删除特定图片
rm static/images/courses/course-*.jpg
```

### Q9: 生成速度慢怎么办？

**A**:
- 单张图片约需 10-15 秒
- 工具已内置 2 秒请求间隔（避免 API 限流）
- 可以分批生成，按优先级处理

### Q10: 如何查看生成进度？

**A**: 工具会实时显示进度：
```
[1/7] Processing: image1.jpg
================================================================================
Generating: image1.jpg
Priority: high
Prompt: ...
Calling API...
Image URL received: ...
Downloading image...
[SUCCESS] Saved to image1.jpg (124.4 KB)
Waiting 2 seconds before next request...
```

---

## 📚 参考资源

### 项目中的配置文件示例

1. **images-example.json** - 基础示例（3张图片）
   ```bash
   cat images-example.json
   ```

2. **course-images.json** - 课程封面配置（7张图片）
   ```bash
   cat course-images.json
   ```

3. **course-images-mapping.json** - 课程映射关系
   ```bash
   cat course-images-mapping.json
   ```

### 相关文档

- **IMAGE_GENERATION_SETUP_REPORT.md** - 图片生成工具配置报告
- **COURSE_IMAGES_GENERATION_REPORT.md** - 课程图片生成完整报告
- **TODO.md** - 项目任务记录

### 生成结果查看

```bash
# 查看已生成的示例图片
ls -lh static/images/generated/

# 查看课程封面图片
ls -lh static/images/courses/

# 查看图片详细信息
file static/images/courses/*.jpg
```

---

## 🛠️ 故障排查

### 环境问题

```bash
# 检查 Python 版本
python3 --version

# 检查依赖
pip list | grep requests

# 重新安装依赖
pip install -r requirements.txt
```

### 网络问题

```bash
# 测试 API 连接
curl -I https://open.bigmodel.cn/api/paas/v4/images/generations

# 使用代理（如需要）
export https_proxy=http://proxy.example.com:8080
```

### 权限问题

```bash
# 检查目录权限
ls -ld static/images/

# 修改权限
chmod 755 static/images/

# 检查文件权限
ls -l tools/generate_images.py

# 添加执行权限
chmod +x tools/generate_images.py
```

---

## 💡 最佳实践

### 1. 配置管理

- ✅ 为不同类型的图片创建独立配置文件
- ✅ 使用有意义的文件名（如 `course-images.json`）
- ✅ 保持配置文件版本控制（Git）
- ✅ 定期备份生成的图片

### 2. 提示词管理

- ✅ 建立提示词模板库
- ✅ 记录成功的提示词案例
- ✅ 为不同场景准备标准描述
- ✅ 持续优化和改进提示词

### 3. 批量生成策略

- ✅ 按优先级分批生成
- ✅ 高优先级图片优先使用
- ✅ 预留时间进行质量检查
- ✅ 建立图片审核流程

### 4. 文件组织

```
static/images/
├── courses/          # 课程封面
├── events/           # 活动图片
├── news/             # 新闻配图
├── team/             # 团队照片
├── gallery/          # 图片画廊
└── generated/        # 其他生成图片
```

### 5. 质量控制

- ✅ 生成后立即检查图片质量
- ✅ 不合适的图片重新生成
- ✅ 保存优质提示词案例
- ✅ 建立图片审核标准

---

## 📞 支持与反馈

### 遇到问题？

1. 查看本文档的[常见问题](#常见问题)部分
2. 检查[故障排查](#故障排查)指南
3. 查看完整报告: `COURSE_IMAGES_GENERATION_REPORT.md`

### 改进建议

如有改进建议，请记录在项目的 `TODO.md` 文件中。

---

**最后更新**: 2025-11-08
**版本**: 1.0.0
**作者**: maxazure
