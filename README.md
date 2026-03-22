# Bilibili UID 检查器

随机生成 7 位 UID 访问 B 站用户空间，自动筛选「乱码英文用户名 + 0 级」的异常账号并记录。

## 视频教程

![https://www.bilibili.com/video/BV1xjAMzsEsB](https://www.bilibili.com/video/BV1xjAMzsEsB)

## 项目结构

```
bilibili_uid_check/
├── bilibili_uid_checker.py      # 主程序
├── start_chrome_windows.bat     # Windows Chrome 启动脚本
├── start_chrome_macos.sh        # macOS Chrome 启动脚本
├── start_chrome_linux.sh        # Linux Chrome 启动脚本
├── result.txt                   # 检查结果输出文件
└── requirements.txt             # Python 依赖
```

## 环境要求

- **Python** 3.7+
- **Google Chrome** 浏览器
- **DrissionPage** Python 库

## 安装

```bash
pip install -r requirements.txt
```

---

## 快速开始

整个流程分两步：**启动 Chrome** → **运行脚本**。

> [!WARNING]
> 启动前请先**完全关闭**所有 Chrome 窗口和进程，否则调试端口无法生效。

### 第一步：启动 Chrome

根据你的操作系统，运行对应的启动脚本。脚本会以 **无用户态 + 调试端口 9222** 的方式启动 Chrome，不会影响你日常的 Chrome 配置。

#### Windows

双击运行 `start_chrome_windows.bat`，或在 CMD 中执行：

```cmd
start_chrome_windows.bat
```

> 脚本会自动检测常见安装路径（`Program Files` / `Program Files (x86)`）。如果 Chrome 安装在非默认位置，请编辑脚本修改路径。

#### macOS

在终端中执行：

```bash
chmod +x start_chrome_macos.sh   # 首次使用需要赋予执行权限
./start_chrome_macos.sh
```

#### Linux

在终端中执行：

```bash
chmod +x start_chrome_linux.sh   # 首次使用需要赋予执行权限
./start_chrome_linux.sh
```

> 脚本会自动检测 `google-chrome`、`google-chrome-stable` 等常见命令。未安装时会提示安装方法。

### 第二步：运行检查程序

Chrome 启动成功后，**另开一个终端窗口**运行：

```bash
# macOS / Linux
python3 bilibili_uid_checker.py

# Windows
python bilibili_uid_checker.py
```

### 操作流程

1. 程序启动后提示输入 **UID 前缀数字**（支持1位或2位，如 `5` 或 `31`）
2. 输入后自动开始循环检查，控制台实时显示结果
3. 符合条件的账号自动写入 `result.txt`
4. 随时按 **Ctrl+C** 停止程序

---

## 筛选规则

必须**同时满足**以下所有条件，账号才会被记录：

| 条件 | 说明 |
|------|------|
| 全小写英文 | 用户名仅由 a-z 组成，无数字、中文、特殊字符 |
| 长度 6~12 | 过短或过长的用户名排除 |
| 辅音占比 > 60% | 乱码用户名通常辅音密集 |
| 无常见英文子串 | 不含 game、love、the、ing 等 100+ 常见单词 |
| 等级 Lv0 | 用户等级必须为 0 级 |

## 输出格式

`result.txt` 中每条记录格式如下：

```
UID: 1234567 | 用户名: xbjulymph
UID: 3987654 | 用户名: fmxhgdxfl
```

---

## 启动参数说明

Chrome 启动脚本中使用了以下参数：

| 参数 | 作用 |
|------|------|
| `--remote-debugging-port=9222` | 开启调试端口，供 Python 脚本连接控制浏览器 |
| `--no-first-run` | 跳过 Chrome 首次运行的欢迎向导 |
| `--no-default-browser-check` | 跳过默认浏览器检查弹窗 |
| `--user-data-dir=<临时路径>` | 使用临时目录作为用户数据目录（无用户态核心参数），不影响日常 Chrome 配置 |

---

## 常见问题

### 连接 Chrome 失败

- 确保运行了对应系统的启动脚本，且 Chrome 窗口已打开
- 确保启动前**完全关闭**了所有旧的 Chrome 进程：
  - **macOS**：在活动监视器中搜索 `Chrome`，全部退出
  - **Windows**：打开任务管理器，结束所有 `chrome.exe` 进程
  - **Linux**：执行 `pkill -f chrome`

### 修改调试端口

默认调试端口为 `9222`。如需更改：

1. 修改启动脚本中的端口号
2. 同时修改 `bilibili_uid_checker.py` 中的 `DEBUGGING_PORT` 变量

### 无法获取用户名或等级

- B 站页面结构可能更新，检查控制台报错信息
- 确保网络正常，页面能完整加载
