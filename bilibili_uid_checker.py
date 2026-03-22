"""
Bilibili UID 检查器
====================
连接本地 Chrome 浏览器，随机生成7位UID访问B站用户空间，
筛选出「乱码英文用户名 + 0级」的账号并记录到 result.txt。

使用前请先以调试端口启动 Chrome：
  /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
"""

import random
import re
import time
import os
from DrissionPage import ChromiumPage, ChromiumOptions


# ======================== 配置 ========================
OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "result.txt")
MIN_DELAY = 2          # 每次请求最小间隔（秒）
MAX_DELAY = 5          # 每次请求最大间隔（秒）
DEBUGGING_PORT = 9222  # Chrome 调试端口


# ======================== 乱码用户名判定 ========================
# 常见英文子串，如果用户名里包含这些，说明可能是真名
COMMON_SUBSTRINGS = [
    "the", "ing", "tion", "ment", "able", "ness", "ful", "less",
    "game", "love", "cool", "star", "fire", "dark", "blue", "king",
    "play", "hero", "wolf", "fox", "cat", "dog", "sky", "moon",
    "sun", "ice", "war", "pro", "max", "boy", "girl", "man",
    "fan", "god", "ace", "top", "big", "red", "hot", "old",
    "new", "one", "two", "day", "way", "eye", "her", "his",
    "you", "not", "all", "can", "out", "use", "how", "its",
    "may", "did", "get", "has", "him", "see", "now", "come",
    "than", "like", "just", "over", "know", "back", "only",
    "good", "some", "time", "very", "when", "with", "make",
    "hand", "high", "keep", "last", "long", "much", "own",
    "say", "she", "too", "any", "same", "tell", "each",
    "bilibili", "bili", "video", "anime", "music", "live",
    "chen", "wang", "zhang", "yang", "huang", "zhao", "zhou",
    "chun", "xiao", "ming", "hong", "feng", "jing", "ying",
    "qing", "long", "ping", "ling", "dong", "song", "tang",
]

VOWELS = set("aeiou")


def is_gibberish_name(name: str) -> bool:
    """
    判断用户名是否为乱码式英文名。
    条件：
      1. 仅由小写英文字母组成
      2. 长度在 6~12 之间
      3. 辅音字母占比 > 60%
      4. 不含常见英文子串
    """
    # 条件1：仅小写英文字母
    if not re.fullmatch(r"[a-z]+", name):
        return False

    # 条件2：长度 6~12
    if not (6 <= len(name) <= 12):
        return False

    # 条件3：辅音占比 > 60%
    consonant_count = sum(1 for ch in name if ch not in VOWELS)
    if consonant_count / len(name) <= 0.60:
        return False

    # 条件4：不含常见英文子串
    name_lower = name.lower()
    for sub in COMMON_SUBSTRINGS:
        if sub in name_lower:
            return False

    return True


# ======================== 等级提取 ========================
def get_user_level(page) -> int:
    """
    从B站用户空间页面提取用户等级。
    等级信息在 <i class="vui_icon sic-BDC_svg-user_level_0 level-icon"> 中，
    通过 class 中的 user_level_X 提取数字。
    """
    try:
        # 主选择器：i.level-icon
        level_elem = page.ele("css:i.level-icon", timeout=5)
        if level_elem:
            cls = level_elem.attr("class") or ""
            match = re.search(r"user_level_(\d)", cls)
            if match:
                return int(match.group(1))

        # 备选：任何包含 user_level_ 的元素
        level_elem = page.ele("css:i[class*='user_level_']", timeout=3)
        if level_elem:
            cls = level_elem.attr("class") or ""
            match = re.search(r"user_level_(\d)", cls)
            if match:
                return int(match.group(1))

        return -1  # 无法识别
    except Exception:
        return -1


# ======================== 用户名提取 ========================
def get_username(page) -> str:
    """从B站用户空间页面提取用户名。"""
    try:
        # 主选择器：div.nickname
        name_elem = page.ele("css:div.nickname", timeout=5)
        if name_elem:
            return name_elem.text.strip()

        # 备选：任何 class 包含 nickname 的元素
        name_elem = page.ele("css:[class*='nickname']", timeout=3)
        if name_elem:
            return name_elem.text.strip()

        return ""
    except Exception:
        return ""


# ======================== 主逻辑 ========================
def main():
    print("=" * 55)
    print("   Bilibili UID 检查器 — 乱码用户名 + 0级 筛选工具")
    print("=" * 55)

    # 1. 让用户选择 UID 第一位数字
    while True:
        first_digit = input("\n请输入 UID 的第一位数字 (1-9): ").strip()
        if first_digit in [str(i) for i in range(1, 10)]:
            first_digit = int(first_digit)
            break
        print("❌ 输入无效，请输入 1~9 之间的数字。")

    # 2. 连接本地 Chrome
    print(f"\n🔗 正在连接本地 Chrome (端口 {DEBUGGING_PORT})...")
    try:
        co = ChromiumOptions()
        co.set_local_port(DEBUGGING_PORT)
        page = ChromiumPage(co)
        print("✅ 成功连接 Chrome 浏览器！")
    except Exception as e:
        print(f"❌ 连接 Chrome 失败: {e}")
        print(f"   请确保已以调试端口启动 Chrome：")
        print(f'   /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port={DEBUGGING_PORT}')
        return

    # 3. 统计
    checked = 0
    found = 0

    print(f"\n🚀 开始检查... (UID 首位: {first_digit})")
    print(f"📁 结果保存至: {OUTPUT_FILE}")
    print("-" * 55)

    try:
        while True:
            # 生成随机7位 UID，首位固定
            remaining = random.randint(0, 999999)
            uid = int(f"{first_digit}{remaining:06d}")

            url = f"https://space.bilibili.com/{uid}"

            try:
                page.get(url)
                time.sleep(1.5)  # 等待页面加载

                username = get_username(page)
                level = get_user_level(page)

                checked += 1

                if not username:
                    print(f"  [{checked}] UID {uid} — ⚠️ 无法获取用户名，跳过")
                elif level == -1:
                    print(f"  [{checked}] UID {uid} — ⚠️ 无法获取等级，跳过")
                else:
                    is_gibberish = is_gibberish_name(username)
                    is_level_0 = (level == 0)

                    status_parts = []
                    if is_gibberish:
                        status_parts.append("乱码名 ✓")
                    if is_level_0:
                        status_parts.append("0级 ✓")

                    if is_gibberish and is_level_0:
                        found += 1
                        # 写入文件
                        with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
                            f.write(f"UID: {uid} | 用户名: {username}\n")
                        print(f"  [{checked}] UID {uid} — 用户名: {username} | 等级: Lv{level} | ✅ 命中！已记录 (累计 {found} 个)")
                    else:
                        reason = f"用户名: {username} | 等级: Lv{level}"
                        print(f"  [{checked}] UID {uid} — {reason} | ❌ 不符合")

            except Exception as e:
                checked += 1
                print(f"  [{checked}] UID {uid} — ⚠️ 访问出错: {e}")

            # 随机延时
            delay = random.uniform(MIN_DELAY, MAX_DELAY)
            time.sleep(delay)

    except KeyboardInterrupt:
        print(f"\n\n{'=' * 55}")
        print(f"🛑 手动停止")
        print(f"   共检查: {checked} 个 UID")
        print(f"   命中数: {found} 个")
        print(f"   结果文件: {OUTPUT_FILE}")
        print(f"{'=' * 55}")


if __name__ == "__main__":
    main()
