import asyncio

from aiogram.utils.chat_action import ChatActionMiddleware

from config import bot
from handlers import dp


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    dp.message.middleware(ChatActionMiddleware())
    asyncio.run(main())
