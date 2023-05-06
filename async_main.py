
import asyncio
import logging.handlers
from pathlib import Path


from config import bot
from handlers import dp

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    log_dir = Path(__file__).parent / 'logs'
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / 'chat_gpt_bot.log'
    rotating_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=10 ** 6,
        backupCount=5, encoding='utf-8'
    )
    logging.basicConfig(
        format='%(asctime)s :: %(name)s:%(lineno)s :: '
               '%(levelname)s :: %(message)s',
        level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler())
    )
    asyncio.run(main())
