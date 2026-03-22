#!/bin/bash
# ============================================
#   Chrome 调试模式启动脚本 (macOS)
# ============================================

CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
TEMP_PROFILE="/tmp/chrome_temp_profile"
DEBUG_PORT=9222

echo "============================================"
echo "  Chrome 调试模式启动脚本 (macOS)"
echo "============================================"
echo ""

# 检查 Chrome 是否存在
if [ ! -f "$CHROME_PATH" ]; then
    echo "[✗] 未找到 Chrome 浏览器"
    echo "    期望路径: $CHROME_PATH"
    echo "    请确认已安装 Google Chrome。"
    exit 1
fi

# 清理旧的临时用户数据目录
if [ -d "$TEMP_PROFILE" ]; then
    echo "[*] 正在清理旧的临时配置文件..."
    rm -rf "$TEMP_PROFILE"
fi

echo "[*] 正在以无用户态 + 调试端口 $DEBUG_PORT 启动 Chrome..."
echo ""

"$CHROME_PATH" \
    --remote-debugging-port=$DEBUG_PORT \
    --no-first-run \
    --no-default-browser-check \
    --user-data-dir="$TEMP_PROFILE" &

echo "[✓] Chrome 已在后台启动！(PID: $!)"
echo ""
echo "[i] 现在可以在另一个终端运行: python3 bilibili_uid_checker.py"
echo "[i] 关闭 Chrome 后此脚本自动退出。"
echo ""

wait
