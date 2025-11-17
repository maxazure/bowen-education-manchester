#!/bin/bash

# 生产服务器部署脚本
# 用于将最新代码和数据库同步到生产服务器

set -e

SERVER="azureuser@bowen.docms.nz"
PROJECT_PATH="/var/www/bowen-education-manchester"
LOCAL_DB="instance/database.db"

echo "=== 博文教育网站生产部署 ==="
echo "目标服务器: $SERVER"
echo "项目路径: $PROJECT_PATH"
echo ""

# 1. 备份服务器数据库
echo "[1/5] 备份服务器数据库..."
ssh $SERVER "cd $PROJECT_PATH && cp $LOCAL_DB ${LOCAL_DB}.backup-\$(date +%Y%m%d-%H%M%S)"
echo "✓ 数据库备份完成"

# 2. 拉取最新代码
echo "[2/5] 拉取最新代码..."
ssh $SERVER "cd $PROJECT_PATH && git pull origin main"
echo "✓ 代码更新完成"

# 3. 上传本地数据库（如果需要）
read -p "是否上传本地数据库到服务器? (y/N): " upload_db
if [[ $upload_db =~ ^[Yy]$ ]]; then
    echo "[3/5] 上传数据库文件..."
    scp $LOCAL_DB $SERVER:$PROJECT_PATH/$LOCAL_DB
    echo "✓ 数据库上传完成"
else
    echo "[3/5] 跳过数据库上传"
fi

# 4. 重启服务
echo "[4/5] 重启应用服务..."
ssh $SERVER "sudo systemctl restart bowen-education.service"
echo "✓ 服务重启完成"

# 5. 验证服务状态
echo "[5/5] 验证服务状态..."
ssh $SERVER "sudo systemctl status bowen-education.service | head -10"

echo ""
echo "=== 部署完成 ==="
echo "请访问 https://bowen.docms.nz 验证网站运行正常"
