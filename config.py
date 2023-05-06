import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

bot = Bot(token=BOT_TOKEN)
