# 图片压缩和分类工具

## 功能说明

这个脚本用于处理"网站文案和照片"目录下的所有图片文件，进行压缩和分类整理到`upload`文件夹。

## 主要功能

1. **格式转换**：将所有图片转换为JPG格式
   - 特别支持HEIC格式（iPhone照片）
   - 支持PNG、GIF、BMP、WebP等格式

2. **图片压缩**：
   - 最大边长限制：1920px（保持原始比例）
   - JPEG质量：85（互联网标准）
   - 自动优化文件大小

3. **智能分类**：
   - 按照原始目录结构分类
   - 中文文件夹名自动转换为英文
   - 输出到`upload`目录的对应子文件夹

## 使用方法

### 安装依赖

```bash
source venv/bin/activate
pip install pillow pillow-heif
```

### 运行脚本

```bash
source venv/bin/activate
python scripts/compress_images.py
```

## 处理效果

根据实际运行结果：

- **总文件数**：448个图片
- **压缩前总大小**：216.37 MB
- **压缩后总大小**：52.00 MB
- **总压缩率**：76.0%

典型压缩效果：
- HEIC → JPG：压缩率 70-90%
- 高清JPG：压缩率 70-85%
- PNG → JPG：压缩率 80-90%

## 文件分类

脚本会将图片按以下类别整理：

```
upload/
├── chess-club/                 (10个文件)
├── parktastic-activities/      (67个文件)
├── chinese-new-year-2025/      (32个文件)
├── government-haf-camp/        (22个文件)
├── christmas-concert/          (8个文件)
├── middleton-summer-camp/      (6个文件)
├── chinese-school/             (3个文件)
└── website-photos/             (300个文件)
    ├── government-camp/
    │   ├── 2021/
    │   ├── 2022/
    │   ├── 2023/
    │   ├── 2024/
    │   └── 2025/
    ├── camp-highlights/
    ├── chess-club/
    ├── christmas-concert/
    └── middleton-summer-camp/
```

## 文件夹映射

中文文件夹 → 英文文件夹的映射关系：

| 中文名称 | 英文名称 |
|---------|---------|
| Chess Club | chess-club |
| parktastic活动 | parktastic-activities |
| 中国新年 2025 | chinese-new-year-2025 |
| 政府项目 假期营 | government-haf-camp |
| 活动 圣诞音乐会 | christmas-concert |
| 活动 米德尔顿夏令营 | middleton-summer-camp |
| 中文学校网站 | chinese-school |
| 网站照片分享 | website-photos |

## 配置参数

可以在脚本中修改以下参数：

```python
MAX_SIZE = 1920      # 最大边长（像素）
QUALITY = 85         # JPEG质量（1-100）
SOURCE_DIR = "网站文案和照片"
OUTPUT_DIR = "upload"
```

## 注意事项

1. **重复处理**：脚本会跳过已存在的文件，可以安全地重复运行
2. **原文件保留**：原始文件不会被修改或删除
3. **PSD文件**：PSD格式的设计文件会被自动跳过
4. **文档文件**：Word文档（.docx）等非图片文件会被忽略

## 输出示例

```
开始处理图片...
源目录: 网站文案和照片
输出目录: upload
最大尺寸: 1920px
JPEG质量: 85
------------------------------------------------------------
✓ 成功: parktastic-20250806-026.heic -> parktastic-20250806-026.jpg (5502.6KB -> 975.2KB, 压缩 82.3%)
✓ 成功: chess-club-004.heic -> chess-club-004.jpg (2751.6KB -> 632.5KB, 压缩 77.0%)
跳过（已存在）: existing-image.jpg
------------------------------------------------------------
处理完成！
总文件数: 448
成功处理: 121
跳过文件: 327
失败文件: 0
总大小（压缩前）: 216.37 MB
总大小（压缩后）: 52.00 MB
总压缩率: 76.0%
```

## 故障排除

### 问题：HEIC文件无法处理

**解决方案**：
```bash
pip install pillow-heif
```

### 问题：内存不足

**解决方案**：处理大量高分辨率图片时，可以降低MAX_SIZE参数或分批处理。

### 问题：颜色失真

**解决方案**：提高QUALITY参数（建议范围：80-95）。

## 性能优化

- 单个图片处理时间：约0.1-0.5秒
- 批量处理448个文件：约30-60秒
- 内存占用：峰值约100-200MB
