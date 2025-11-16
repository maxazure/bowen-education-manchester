## 数据库同步操作指南

### 服务器信息
- **服务器地址**: 192.168.31.205
- **SSH用户**: maxazure
- **项目路径**: /home/maxazure/projects/bowen-education-manchester
- **服务名称**: bowen-education.service
- **服务端口**: 10034

### 同步数据库标准流程

每次同步数据库到服务器时,请按以下步骤操作:

```bash
# 1. 备份服务器现有数据库(带时间戳)
ssh maxazure@192.168.31.205 "cd /home/maxazure/projects/bowen-education-manchester && cp instance/database.db instance/database.db.backup.$(date +%Y%m%d_%H%M%S)"

# 2. 上传本地数据库到服务器
scp instance/database.db maxazure@192.168.31.205:/home/maxazure/projects/bowen-education-manchester/instance/

# 3. 重启服务使更改生效
ssh maxazure@192.168.31.205 "sudo systemctl restart bowen-education.service"

# 4. 验证服务状态
ssh maxazure@192.168.31.205 "sudo systemctl status bowen-education.service --no-pager"
```

### 注意事项
- 同步前必须先备份服务器现有数据库
- 备份文件命名格式: `database.db.backup.YYYYMMDD_HHMMSS`
- 上传后必须重启服务才能生效
- 验证服务状态确保重启成功

### 常用服务器命令

```bash
# 查看服务状态
ssh maxazure@192.168.31.205 "sudo systemctl status bowen-education.service"

# 查看服务日志
ssh maxazure@192.168.31.205 "sudo journalctl -u bowen-education.service -n 50"

# 查看访问日志
ssh maxazure@192.168.31.205 "tail -f /home/maxazure/projects/bowen-education-manchester/logs/access.log"

# 查看错误日志
ssh maxazure@192.168.31.205 "tail -f /home/maxazure/projects/bowen-education-manchester/logs/error.log"

# 查看数据库备份列表
ssh maxazure@192.168.31.205 "ls -lh /home/maxazure/projects/bowen-education-manchester/instance/database.db*"
```

## 其他注意事项

- 在使用 chrome devtool 截图的时候应当保存为 jpg 格式并且不要尝试全屏截图,确保图片尺寸不超过8000px