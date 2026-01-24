#!/bin/bash
# 注意：去掉 -e，这样即使 curl 失败，我们也能记录错误而不是直接崩溃
set -ux

URL="https://crop-disease-recognition-and-control-system-release.streamlit.app/"
LOG_FILE="visit_log.log"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# 获取北京时间
TIMESTAMP=$(TZ=Asia/Shanghai date '+%Y-%m-%d %H:%M:%S')

echo "--- Visit Start: $TIMESTAMP ---" >> $LOG_FILE

# 执行请求并捕获 HTTP 状态码
# -o /dev/null: 不保存网页正文
# -w "%{http_code}": 只输出状态码
# -I: 发送 HEAD 请求（如果不行，可改为 -L）
HTTP_STATUS=$(curl -L -k -s -I -o /dev/null -w "%{http_code}" \
  -H "User-Agent: $UA" \
  "$URL")

# 构造结果行
RESULT_LINE="[$TIMESTAMP] URL: $URL | Status: $HTTP_STATUS"

# 1. 写入 log 文件
echo "$RESULT_LINE" >> $LOG_FILE

# 2. 打印到控制台（这样你在 GitHub Action 的 Run 记录里就能直接看到）
echo "******************************************"
echo "  HTTP STATUS: $HTTP_STATUS"
echo "******************************************"
echo "$RESULT_LINE"

# 3. 简单的逻辑检查
if [ "$HTTP_STATUS" -eq 200 ]; then
    echo "Success: Website is awake."
else
    echo "Warning: Received status $HTTP_STATUS"
    # 如果你想让 Action 在失败时显示红色叉叉，可以取消下面这行的注释
    # exit 1
fi
