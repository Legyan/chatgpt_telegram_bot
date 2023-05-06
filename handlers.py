import logging

from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

from openai_requests import get_answer_from_chatgpt4

dp = Dispatcher()


@dp.message(Command('start'))
async def start_handler(msg: Message):
    await msg.answer(f'Привет {msg.from_user.username}! '
                     f'Этот бот позволяет общаться с ChatGPT 4 через API OPENAI. '
                     f'Напишите что нибудь и бот пришлёт вам ответ от ChatGPT.')


@dp.message()
async def message_handler(msg: Message):
    name = msg.from_user.username
    message = msg.text
    if not message:
        return
    logging.info(name + ' написал:\n' + message)
    try:
        gpt_response = await get_answer_from_chatgpt4(message, name)
        await msg.answer(gpt_response)
    except Exception as error:
        logging.info(f'Error: {error}')
        await msg.answer('Запрос к OpenAI не получил ответа, попробуйте позже.')

