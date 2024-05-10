import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import FSInputFile

from config import settings

from database.models import async_main
from data_parsing.data_parsing import parsing
from data_parsing.xlsx_file_creating import xlsx_creating

bot = Bot(token=settings.telebot_token.get_secret_value())
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: types.Message) -> None:
    await message.reply("Hello, I'm a bot assistant with exchange rates.\n\n"
                        "I can display the USD-UAH exchange rates for today.\n\n"
                        "I am using data from the following site:\n"
                        "https://www.google.com/finance/quote/USD-UAH")


@dp.message(Command("get_exchange_rate"))
async def echo(message: types.Message) -> None:
    try:
        await parsing()
        await xlsx_creating()
        file = FSInputFile("data_parsing/exchange_rates/exchange_rates.xlsx")
        await message.answer_document(file)
    except IndexError:
        await message.answer("Today there was no data on exchange rates yet.")
    except Exception as e:
        print(f"Error: {e}")


async def bot_run() -> None:
    await async_main()
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(bot_run())
    except KeyboardInterrupt:
        print("Bot turns off!")
