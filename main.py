import asyncio

from telegram_bot.core import bot_run

if __name__ == "__main__":
    try:
        asyncio.run(bot_run())
    except KeyboardInterrupt:
        print("Bot turns off!")
