# /bin/zsh

# 工程目录设置
PROJECT_DIR=$(cd $(dirname $0); pwd)
echo "\033[35m 当前工程目录为${PROJECT_DIR} \033[0m"
DIST_DIT="${PROJECT_DIR}/dist/"
echo "\033[35m 当前编译目录为${DIST_DIT} \033[0m"

# 压缩文件名设置
CUR_DATATIME="`date +%Y-%m-%d_%H-%M`"
ZIP_NAME="${CUR_DATATIME}.zip"

# 服务器设置
SSH_HOST=""
SSH_USER=""
SSH_PASSWORD=""
# 部署目录
REMOTE_DIR=""


echo "\033[32m 开始部署文件，现在进行打包 \033[0m"
cd $PROJECT_DIR
(npm run build:prod) >/dev/null 2>&1
echo "\033[32m 打包完成 \033[0m"
echo "\033[32m 开始压缩文件 \033[0m"
cd $DIST_DIT
zip -q -r $ZIP_NAME ./

echo "\033[32m 压缩完成，文件名  ${ZIP_NAME} \033[0m"
echo "\033[32m 开始传输文件 \033[0m"

(expect -c "
spawn scp $ZIP_NAME "${SSH_USER}@${SSH_HOST}:${REMOTE_DIR}"
expect \"password:\"
send \"${SSH_PASSWORD}\r\"
expect eof
") >/dev/null 2>&1

echo "\033[32m 传送完成，传送到服务器目录：${REMOTE_DIR}${ZIP_NAME} \033[0m"
echo "\033[32m 开始部署 \033[0m"

(expect -c "
spawn ssh -t "${SSH_USER}:${SSH_PASSWORD}@${SSH_HOST}"
set timeout 3
expect \"password:\"
send \"${SSH_PASSWORD}\r\"
expect \"\$\"
send \"cd ${REMOTE_DIR}\r\"
expect \"\$\"
send \"rm -rf html static .DS_Store && rm -f index.html favicon.ico robots.txt\r\"
expect \"\$\"
send \"unzip ${ZIP_NAME}\r\"
expect \"\$\"
send \"exit\r\"
expect eof
# ") >/dev/null 2>&1

echo "\033[32m 部署完成 \033[0m"

