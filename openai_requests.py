import logging

import openai

from config import OPENAI_KEY

openai.api_key = OPENAI_KEY


async def get_answer_from_chatgpt4(message, name):
    logging.info('Отправлен запрос в OpenAI')
    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[
            {"role": 'user', "content": name + ' пишет:\n' + message},
        ]
    )
    text_response = response['choices'][0]['message']['content'].strip()
    logging.info(f'Получен ответ от OpenAI:\n{text_response}')
    return text_response
