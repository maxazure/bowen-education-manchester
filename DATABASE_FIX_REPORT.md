# 数据库数据一致性修复报告
Database Data Consistency Fix Report

**项目名称**: Bowen Education Manchester
**修复日期**: 2025-11-16
**执行人**: maxazure
**数据库**: SQLite 3 (instance/database.db)

---

## 一、修复概览 Summary

本次修复共完成 **4项** 数据一致性问题的修正：
- 重复栏目名称修复: 2项
- 联系信息统一: 2项

所有修复均已验证成功，数据库数据一致性良好。

---

## 二、修复详情 Details

### 1. 重复栏目名称修复 (2项)

**问题描述**:
- 数据库中发现 "课程设置" 名称重复出现2次
- 位于不同的栏目下（中文学校 和 国际象棋俱乐部）
- 这会导致用户界面混淆和数据管理困难

**修复方案**:
根据栏目的 slug 和父栏目，重命名以区分：

| 栏目ID | 原名称 | 新名称 | Slug | 父栏目 |
|-------|--------|--------|------|--------|
| 13 | 课程设置 | **中文学校课程设置** | school-curriculum | 中文学校 (ID: 3) |
| 27 | 课程设置 | **国际象棋课程设置** | chess-courses | 国际象棋俱乐部 (ID: 5) |

**SQL更新**:
```sql
UPDATE site_column
SET name = '中文学校课程设置', updated_at = CURRENT_TIMESTAMP
WHERE id = 13;

UPDATE site_column
SET name = '国际象棋课程设置', updated_at = CURRENT_TIMESTAMP
WHERE id = 27;
```

**验证结果**:
```
✓ ID: 13, Name: 中文学校课程设置, Slug: school-curriculum
✓ ID: 27, Name: 国际象棋课程设置, Slug: chess-courses
```

---

### 2. 联系信息统一 (2项)

**问题描述**:
- 数据库中的联系信息与 README.md 中的官方信息不一致
- 电话号码格式不统一
- 邮箱域名不正确

**官方联系信息** (来自 README.md):
- 电话: `0161 969 3071`
- 邮箱: `info@boweneducation.co.uk`
- 地址: `1/F, 2A Curzon Road, Sale, Manchester M33 7DR, UK`

#### 2.1 电话号码修复

| Setting Key | 原值 | 新值 |
|------------|------|------|
| company_phone | +44 (0)161 6672668 | **0161 969 3071** |
| phone | 0161 969 3071 | 0161 969 3071 (无需修改) |

**SQL更新**:
```sql
UPDATE site_setting
SET value_text = '0161 969 3071', updated_at = CURRENT_TIMESTAMP
WHERE setting_key = 'company_phone';
```

#### 2.2 邮箱地址修复

| Setting Key | 原值 | 新值 |
|------------|------|------|
| company_email | info@boweneducation.org | **info@boweneducation.co.uk** |

**SQL更新**:
```sql
UPDATE site_setting
SET value_text = 'info@boweneducation.co.uk', updated_at = CURRENT_TIMESTAMP
WHERE setting_key = 'company_email';
```

**验证结果**:
```
✓ company_phone: 0161 969 3071
✓ phone: 0161 969 3071
✓ company_email: info@boweneducation.co.uk
✓ company_address: 1/F, 2A Curzon Road, Sale, Manchester, M33 7DR, UK
```

---

## 三、数据一致性检查 Data Consistency Check

### 3.1 栏目数据检查

**检查项目**:
- [x] 重复栏目名称检查
- [x] 重复 slug 检查
- [x] 启用状态检查
- [x] 日期字段检查

**检查结果**:
```
✓ 总栏目数: 31个
✓ 重复名称: 0个 (已修复)
✓ 重复 slug: 0个
✓ 启用状态: 31个启用, 0个禁用
✓ 日期字段: 全部正常，无空值
```

### 3.2 产品/课程引用检查

**检查内容**: 检查 product 表中的 column_id 是否引用了有效的栏目

**检查结果**:
```
✓ 总产品数: 7个
✓ 所有产品的栏目引用都有效
✓ 栏目分布:
  - 中文学校 (ID: 3): 5个课程
  - 补习中心 (ID: 4): 2个课程
```

**产品列表**:
1. Foundation Mandarin (Ages 5-7) → 中文学校
2. GCSE Chinese (Ages 14-16) → 中文学校
3. A-Level Chinese (Ages 16-18) → 中文学校
4. HSK Level 3 Preparation → 中文学校
5. Cantonese Language Course → 中文学校
6. GCSE Mathematics Tutoring → 补习中心
7. A-Level Physics Tutoring → 补习中心

### 3.3 文章引用检查

**检查内容**: 检查 post 表中的 column_id 是否引用了有效的栏目

**检查结果**:
```
✓ 总文章数: 21篇
✓ 所有文章的栏目引用都有效
✓ 栏目分布:
  - 博文新闻 (ID: 8): 4篇
  - 中文学校课程设置 (ID: 13): 7篇
  - 活动与赛事 (ID: 16): 3篇
  - 赛事活动 (ID: 19): 3篇
  - 公园活动 (ID: 23): 1篇
  - 新闻与精彩回顾 (ID: 29): 3篇
```

---

## 四、修复统计 Statistics

| 类别 | 数量 | 状态 |
|-----|------|------|
| 重复栏目名称 | 2个 | ✓ 已修复 |
| 错误电话号码 | 1条 | ✓ 已修复 |
| 错误邮箱地址 | 1条 | ✓ 已修复 |
| **总计** | **4项** | **✓ 全部完成** |

**涉及数据库表**:
- `site_column` - 栏目表
- `site_setting` - 站点设置表

---

## 五、技术实现 Technical Implementation

### 5.1 修复工具

创建了专门的数据修复脚本: `/Users/maxazure/projects/bowen-education-manchester/fix_database.py`

**脚本功能**:
1. 检查并修复重复栏目名称
2. 检查并统一联系信息
3. 全面检查数据一致性
4. 验证修复结果
5. 生成详细报告

### 5.2 执行方式

```bash
# 激活虚拟环境
source venv/bin/activate

# 运行修复脚本
python fix_database.py
```

### 5.3 安全措施

- 使用事务机制，确保数据修改的原子性
- 修改前进行详细检查和验证
- 保留修复日志，记录所有变更
- 修复后立即验证结果

---

## 六、验证结果 Verification

### 6.1 栏目名称验证

```sql
SELECT id, name, slug FROM site_column
WHERE slug IN ('school-curriculum', 'chess-courses');
```

结果:
```
✓ ID: 13, Name: 中文学校课程设置, Slug: school-curriculum
✓ ID: 27, Name: 国际象棋课程设置, Slug: chess-courses
```

### 6.2 联系信息验证

```sql
SELECT setting_key, value_text FROM site_setting
WHERE setting_key IN ('company_email', 'company_phone', 'company_address', 'phone')
ORDER BY setting_key;
```

结果:
```
✓ company_address: 1/F, 2A Curzon Road, Sale, Manchester, M33 7DR, UK
✓ company_email: info@boweneducation.co.uk
✓ company_phone: 0161 969 3071
✓ phone: 0161 969 3071
```

### 6.3 数据一致性验证

```sql
-- 检查是否还有重复名称
SELECT name, COUNT(*) as count FROM site_column
GROUP BY name HAVING count > 1;
```

结果:
```
✓ 无重复栏目名称
```

---

## 七、后续建议 Recommendations

### 7.1 数据维护

1. **定期检查数据一致性**
   - 建议每月运行一次数据一致性检查
   - 可以定期运行 `fix_database.py` 脚本进行检查

2. **联系信息管理**
   - 所有联系信息应统一在 `site_setting` 表中维护
   - 确保与官方文档 (README.md) 保持一致

3. **栏目命名规范**
   - 避免使用相同的栏目名称
   - 建议在栏目名称中包含父栏目信息以区分
   - 使用清晰、描述性的名称

### 7.2 数据库约束

建议添加以下数据库约束（未来优化）:

```sql
-- 1. 为 site_column 表添加唯一约束
CREATE UNIQUE INDEX idx_unique_column_name ON site_column(name);

-- 2. 为 site_setting 表添加唯一约束
CREATE UNIQUE INDEX idx_unique_setting_key ON site_setting(setting_key);
```

### 7.3 数据备份

建议在进行任何数据修改前：
1. 备份数据库文件
2. 记录修改日志
3. 验证修改结果

---

## 八、总结 Conclusion

本次数据一致性修复工作已顺利完成，共修复了 **4项** 数据问题：

1. ✓ 重复栏目名称已全部重命名并区分
2. ✓ 联系信息已统一为官方正确信息
3. ✓ 数据一致性检查通过，无其他问题
4. ✓ 所有修复已验证成功

**数据库当前状态**: ✓ 良好

**建议**:
- 保留 `fix_database.py` 脚本用于日常维护
- 定期检查数据一致性
- 遵循数据命名规范

---

**报告生成时间**: 2025-11-16
**报告生成人**: maxazure
**报告版本**: 1.0
