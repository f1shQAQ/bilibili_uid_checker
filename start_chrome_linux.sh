#!/bin/bash
# ============================================
#   Chrome 调试模式启动脚本 (Linux)
# ============================================

TEMP_PROFILE="/tmp/chrome_temp_profile"
DEBUG_PORT=9222

echo "============================================"
echo "  Chrome 调试模式启动脚本 (Linux)"
echo "============================================"
echo ""

# 检测 Chrome 安装路径
CHROME_PATH=""
for candidate in \
    "google-chrome" \
    "google-chrome-stable" \
    "/opt/google/chrome/google-chrome" \
    "/usr/bin/google-chrome" \
    "/usr/bin/google-chrome-stable"; do
    if command -v "$candidate" &>/dev/null || [ -x "$candidate" ]; then
        CHROME_PATH="$candidate"
        break
    fi
done

if [ -z "$CHROME_PATH" ]; then
    echo "[✗] 未找到 Chrome 浏览器，请先安装 Google Chrome。"
    echo "    安装方法 (Debian/Ubuntu):"
    echo "      wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"
    echo "      sudo dpkg -i google-chrome-stable_current_amd64.deb"
    echo "      sudo apt-get install -f"
    exit 1
fi

echo "[*] 检测到 Chrome: $CHROME_PATH"

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
