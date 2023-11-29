from aiogram import Bot, Dispatcher, Bot
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
bot_token = os.getenv("Bot_TOKEN")

bot = Bot(token=bot_token)
dispatcher = Dispatcher()

async def main() -> None:
    """
    Entry point
    """
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())