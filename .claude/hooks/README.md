# Claude Code Hooks - 自动化任务执行系统

## 概述

这个目录包含Claude Code的hook脚本，用于自动化和增强开发工作流。

## 已配置的Hooks

### 1. Auto-Continue Hook (auto_continue.py)

**触发时机**: 每次使用TodoWrite工具后

**功能**:
- 📊 显示任务进度统计
- 🎯 检测任务完成事件
- 🤖 自动提示继续下一个pending任务
- ✅ 任务全部完成时显示庆祝消息

**工作流程**:
```
1. 用户/Claude更新Todos → TodoWrite工具调用
2. Hook触发 → auto_continue.py执行
3. 分析任务状态变化
4. 如果有任务刚完成且存在pending任务
   → 输出明确指令让Claude继续下一个任务
5. Claude接收指令 → 自动开始下一个任务
6. 循环直到所有任务完成
```

**示例输出**:
```
============================================================
📋 Todo List Status Update
============================================================
✅ Completed: 7/10
🔄 In Progress: 0/10
⏳ Pending: 3/10
============================================================

🎯 TASK COMPLETED! Moving to next task...

📌 Next Task: Phase 6: 自动化测试

======================================================================
🤖 AUTO-CONTINUE INSTRUCTION
======================================================================

Please continue with the next pending task:

  Task: Phase 6: 自动化测试
  Status: pending

Mark this task as 'in_progress' and begin execution immediately.
Do NOT wait for user confirmation. Continue automatically.
======================================================================
```

### 2. Test Checker Hook (test_checker.py)

**触发时机**: 每次Bash命令执行后

**功能**:
- 检查项目是否为Python项目
- 检查是否存在tests目录
- 静默执行，不阻塞工作流

**用途**: 可扩展为自动运行测试、代码质量检查等

## Hook配置文件

### hooks.json

```json
{
  "hooks": {
    "PostToolUse:TodoWrite": {
      "description": "Auto-continue to next pending task",
      "command": "python .claude/hooks/auto_continue.py TodoWrite '{\"todos\": $TOOL_ARGS}'",
      "blocking": false,
      "enabled": true
    },
    "PostToolUse:Bash": {
      "description": "Test checker",
      "command": "python .claude/hooks/test_checker.py",
      "blocking": false,
      "enabled": true
    }
  }
}
```

## 文件说明

```
.claude/hooks/
├── README.md              # 本文档
├── hooks.json             # Hook配置文件
├── auto_continue.py       # 自动继续执行hook
├── test_checker.py        # 测试检查hook
└── .todos_cache.json      # Todos状态缓存 (自动生成)
```

## 使用方法

### 启用自动化任务执行

Hooks已默认启用。每次使用TodoWrite更新任务时，系统会自动：

1. 检测任务完成
2. 查找下一个待办任务
3. 提示Claude继续执行

### 禁用Auto-Continue Hook

如果您想手动控制任务执行，编辑`hooks.json`:

```json
{
  "hooks": {
    "PostToolUse:TodoWrite": {
      "enabled": false  // 改为false
    }
  }
}
```

### 调试Hook

查看hook输出（stderr）:
```bash
# Hook的输出会显示在终端的stderr中
# 通常以 🎯 🤖 📋 等emoji开头
```

查看Todos缓存:
```bash
cat .claude/hooks/.todos_cache.json
```

## 工作原理

### Auto-Continue Hook流程

```python
1. 接收TodoWrite工具的参数
2. 加载上次保存的todos状态（.todos_cache.json）
3. 比较前后状态，检测任务完成
4. 统计各状态任务数量
5. 查找下一个pending任务
6. 如果检测到完成 + 存在pending任务:
   → 输出强提示指令到stderr
   → Claude看到指令后自动继续
7. 保存当前状态供下次比较
```

### 状态检测逻辑

**任务完成检测**:
- 比较in_progress任务数量（减少=完成）
- 比较completed任务数量（增加=完成）

**自动继续条件**:
```python
if task_just_completed and next_pending_task_exists:
    prompt_claude_to_continue()
```

## 扩展Hook系统

### 添加新的Hook

1. 创建Python脚本:
```bash
touch .claude/hooks/my_new_hook.py
chmod +x .claude/hooks/my_new_hook.py
```

2. 添加到hooks.json:
```json
{
  "hooks": {
    "PostToolUse:MyTool": {
      "description": "My custom hook",
      "command": "python .claude/hooks/my_new_hook.py",
      "blocking": false,
      "enabled": true
    }
  }
}
```

### 可用的Hook触发点

- `PostToolUse:TodoWrite` - TodoWrite工具调用后
- `PostToolUse:Bash` - Bash命令执行后
- `PostToolUse:Read` - 读取文件后
- `PostToolUse:Write` - 写入文件后
- `PostToolUse:Edit` - 编辑文件后
- 等等...

## 最佳实践

### ✅ 推荐做法

1. **保持Hook快速执行** - Hook应在<1秒内完成
2. **使用非阻塞模式** - `"blocking": false`避免中断工作流
3. **输出到stderr** - 使用`print(..., file=sys.stderr)`
4. **优雅失败** - 捕获异常，始终`sys.exit(0)`
5. **添加日志** - 重要事件记录到文件

### ❌ 避免做法

1. ❌ 长时间运行的hook（>5秒）
2. ❌ 阻塞式hook（除非必要）
3. ❌ 修改工作目录
4. ❌ 输出到stdout（会干扰工具输出）
5. ❌ 未处理的异常

## 故障排除

### Hook不执行

1. 检查文件权限:
```bash
ls -la .claude/hooks/*.py
# 应显示 -rwxrwxr-x (可执行)
```

2. 检查Python路径:
```bash
which python
python --version
```

3. 手动测试hook:
```bash
python .claude/hooks/auto_continue.py TodoWrite '{"todos": [{"content": "Test", "status": "pending", "activeForm": "Testing"}]}'
```

### 自动继续不工作

1. 检查hook是否启用（hooks.json）
2. 查看.todos_cache.json是否更新
3. 确认pending任务存在

### 查看详细日志

临时启用详细日志:
```json
{
  "settings": {
    "verbose_logging": true
  }
}
```

## 示例场景

### 场景1: 连续执行10个任务

```
初始状态:
- Task 1-7: completed
- Task 8: in_progress
- Task 9-10: pending

1. Task 8完成 → TodoWrite更新
2. Hook检测完成 → 找到Task 9
3. 输出指令 → Claude看到
4. Claude自动开始Task 9
5. Task 9完成 → 重复2-4
6. Task 10完成 → 显示🎉庆祝
```

### 场景2: 手动控制

```
如果想手动控制:
1. 禁用auto_continue hook
2. 或者: 暂时不使用TodoWrite
3. 或者: 明确告诉Claude "停止自动执行"
```

## 版本历史

- **v1.0** (2025-11-04)
  - ✅ 初始版本
  - ✅ Auto-continue hook
  - ✅ Test checker hook
  - ✅ Todos缓存机制
  - ✅ 任务完成检测

## 维护者

Bowen Education Group 项目团队

---

**Last Updated**: 2025-11-04
**Hook System Version**: 1.0
