BOT_NAME = 'gold_one_computer'

SPIDER_MODULES = ['gold_one_computer.spiders']
NEWSPIDER_MODULE = 'gold_one_computer.spiders'

# 🚫 Don’t obey robots.txt (Amazon blocks bots in there)
ROBOTSTXT_OBEY = False

# 🕵️ Use middleware
DOWNLOADER_MIDDLEWARES = {
    'gold_one_computer.middlewares.RotateUserAgentMiddleware': 543,
}

# ⏱ Slow it down to look human
DOWNLOAD_DELAY = 2
RANDOMIZE_DOWNLOAD_DELAY = True

# 🔡 Export properly
FEED_EXPORT_ENCODING = 'utf-8'

# 📉 Quiet logs
LOG_LEVEL = 'INFO'
