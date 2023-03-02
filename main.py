import logging.handlers
import os
from pathlib import Path

import openai
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv

load_dotenv()

secret_token = os.getenv('BOT_TOKEN')

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


def get_answer_from_chatgpt(message, name):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    logging.info('Отправлен запрос в OpenAI')
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": 'user', "content": name + ' пишет:\n' + message},
        ]
    )
    text_response = response['choices'][0]['message']['content'].strip()
    logging.info(f'Получен ответ от OpenAI:\n{text_response}')
    return text_response


def chat_with_chatgpt(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    message = update.message.text
    if not message:
        return
    logging.info(name + ' написал\n' + message)
    try:
        gpt_response = get_answer_from_chatgpt(message, name)
    except Exception:
        logging.info('Запрос к OpenAI не получил ответа.')
        return
    context.bot.send_message(chat_id=chat.id, text=gpt_response)


def possibilities(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    message = update.message.text
    button = ReplyKeyboardRemove()
    try:
        gpt_response = get_answer_from_chatgpt(message, name)
    except Exception:
        logging.info('Запрос к OpenAI не получил ответа.')
        return
    context.bot.send_message(
        chat_id=chat.id,
        text=gpt_response,
        reply_markup=button
    )


def wake_up(update, context):
    """Обработчик поступившей команды /start."""
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup(
        [['ChatGPT, что ты умеешь?']], resize_keyboard=True
        )

    context.bot.send_message(
        chat_id=chat.id,
        text='Привет, {}. Чем могу помочь?'.format(name),
        reply_markup=button
    )


def main():
    updater = Updater(token=secret_token)
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.regex('ChatGPT, что ты умеешь?'), possibilities)
    )
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text, chat_with_chatgpt)
        )
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
