# 黄金9999实时数据推送到 Telegram

## 作用

本项目用于北京时间9-22内定时获取 **上海黄金交易所黄金9999** 的实时行情数据，并通过 Telegram Bot 将数据推送到指定的 Telegram 频道或群组。

数据来源：[上海黄金交易所黄金9999实时行情](https://quote.cngold.org/gjs/jjs.html)

## 使用方法

### 1. Fork 项目

点击页面右上角的 **Fork** 按钮，将此项目 Fork 到您的 GitHub 账户。

### 2. 配置 GitHub Actions

1. **克隆仓库**到本地，或者在 GitHub 上直接修改工作流配置文件。
2. 在 GitHub 仓库的 **Settings > Secrets** 中添加以下环境变量：

   * **TG_BOT_TOKEN**：您的 Telegram Bot Token。
   * **TG_CHAT_ID**：您要将数据推送到的 Telegram 频道或群组的 Chat ID。

### 3. 获取 Telegram Bot Token 和 Chat ID

* **创建 Telegram Bot**：搜索 **BotFather**，使用 `/newbot` 命令创建一个新 Bot，获取 `bot token`。
* **获取 Chat ID**：

  1. 向您创建的 Bot 发送一条消息。
  2. 使用以下 API 获取 `chat_id`：

     ```bash
     https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
     ```

     替换 `<YOUR_BOT_TOKEN>` 为您的 Bot Token，返回的数据中会包含您的 `chat_id`。

### 4. 配置 GitHub Actions 定时任务

GitHub Actions 配置文件已经设置为每 **30 分钟** 执行一次，且仅在北京时间 **9:00 AM 到 10:00 PM** 之间触发。

### 5. 手动运行

如果您需要手动运行脚本，可以通过以下命令：

```bash
python fetch_gold.py
```

## 文件结构

```
.
├── .github/
│   └── workflows/
│       └── fetch_gold.yml     # GitHub Actions 配置文件
├── fetch_gold.py              # 主脚本文件
├── requirements.txt           # Python 依赖库
└── README.md                  # 项目文档
```
