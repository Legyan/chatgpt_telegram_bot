import os
from pathlib import Path
import logging.handlers

from aiogram import Bot
from dotenv import load_dotenv


log_dir = Path(__file__).parent / 'logs'
log_dir.mkdir(exist_ok=True)
log_file = log_dir / 'chat_gpt_bot.log'
rotating_handler = logging.handlers.RotatingFileHandler(
    log_file, maxBytes=10 ** 6,
    backupCount=5, encoding='utf-8'
)

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

bot = Bot(token=BOT_TOKEN)
