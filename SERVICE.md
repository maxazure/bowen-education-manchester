# Bowen Education 服务管理说明

## 服务信息

- **服务名称**: bowen-education.service
- **端口**: 10034
- **运行模式**: Production
- **工作进程数**: 4 个 worker
- **自动启动**: 已启用（开机自动运行）
- **日志位置**:
  - 访问日志: `logs/access.log`
  - 错误日志: `logs/error.log`

## 服务管理命令

### 查看服务状态
```bash
sudo systemctl status bowen-education.service
```

### 启动服务
```bash
sudo systemctl start bowen-education.service
```

### 停止服务
```bash
sudo systemctl stop bowen-education.service
```

### 重启服务
```bash
sudo systemctl restart bowen-education.service
```

### 重新加载配置（无需停止服务）
```bash
sudo systemctl reload bowen-education.service
```

### 禁用自动启动
```bash
sudo systemctl disable bowen-education.service
```

### 启用自动启动
```bash
sudo systemctl enable bowen-education.service
```

## 查看日志

### 实时查看服务日志
```bash
sudo journalctl -u bowen-education.service -f
```

### 查看最近的日志
```bash
sudo journalctl -u bowen-education.service -n 100
```

### 查看应用访问日志
```bash
tail -f logs/access.log
```

### 查看应用错误日志
```bash
tail -f logs/error.log
```

## 访问网站

- 本地访问: http://localhost:10034
- 网络访问: http://YOUR_SERVER_IP:10034

## 更新代码后的操作

当更新代码后，需要重启服务使更改生效：

```bash
cd /home/maxazure/projects/bowen-education-manchester
git pull  # 如果使用git
sudo systemctl restart bowen-education.service
```

## 修改服务配置

如果需要修改服务配置（如端口、worker数量等）：

1. 编辑服务文件:
```bash
sudo nano /etc/systemd/system/bowen-education.service
```

2. 重新加载 systemd 配置:
```bash
sudo systemctl daemon-reload
```

3. 重启服务:
```bash
sudo systemctl restart bowen-education.service
```

## 常见端口配置

如果需要更改端口，在服务文件中修改 `--bind 0.0.0.0:PORT` 这一行。

当前配置: `--bind 0.0.0.0:10034`

## 性能调优

### 调整 Worker 数量
在服务文件中修改 `--workers 4` 这一行。

推荐配置:
- CPU核心数 x 2 + 1
- 例如: 4核CPU建议使用 9 workers

### 调整超时时间
如果请求处理时间较长，可以添加:
```
--timeout 120
```

## 故障排查

### 服务无法启动
```bash
# 查看详细错误信息
sudo journalctl -u bowen-education.service -n 50 --no-pager

# 检查端口是否被占用
sudo netstat -tulpn | grep 10034
```

### 服务运行但无法访问
```bash
# 检查防火墙
sudo ufw status
sudo ufw allow 10034

# 或使用 firewalld
sudo firewall-cmd --permanent --add-port=10034/tcp
sudo firewall-cmd --reload
```

### 内存占用过高
```bash
# 查看内存使用情况
sudo systemctl status bowen-education.service

# 减少 worker 数量
# 编辑服务文件，将 --workers 4 改为更小的值
```

## 卸载服务

如果需要移除服务:

```bash
# 停止并禁用服务
sudo systemctl stop bowen-education.service
sudo systemctl disable bowen-education.service

# 删除服务文件
sudo rm /etc/systemd/system/bowen-education.service

# 重新加载 systemd
sudo systemctl daemon-reload
```

## 备份建议

定期备份以下内容:
- 数据库: `instance/database.db`
- 上传文件: `upload/` 目录
- 配置文件: `.env` (如果有)
- 静态文件: `templates/static/images/` (如有自定义内容)

---

**服务已配置完成，重启电脑后会自动运行！**
