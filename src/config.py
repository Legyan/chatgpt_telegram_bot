import logging.handlers
import os
from pathlib import Path

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

log_dir = Path(__file__).parent.parent / 'logs'
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

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
OPENAI_KEY = os.getenv('OPENAI_API_KEY')
ADMINS_ACCOUNTS = os.getenv('ADMINS_ACCOUNTS')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
