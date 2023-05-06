import asyncio
import logging

from config import bot, rotating_handler
from handlers import dp


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s :: %(name)s:%(lineno)s :: '
               '%(levelname)s :: %(message)s',
        level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler())
    )
    asyncio.run(main())
