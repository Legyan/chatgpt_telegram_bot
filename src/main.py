import asyncio

from aiogram.utils.chat_action import ChatActionMiddleware

from config import bot
from handlers import admins_router, dp, whitelist_users_router
from middlewares import (AdminMiddleware, LoggingMiddleware,
                         UserInWhiteListMiddleware)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    admins_router.message.middleware(AdminMiddleware())
    whitelist_users_router.message.middleware(UserInWhiteListMiddleware())
    dp.include_routers(admins_router, whitelist_users_router)
    dp.message.middleware(ChatActionMiddleware())
    dp.message.middleware(LoggingMiddleware())
    asyncio.run(main())
