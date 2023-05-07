import logging

import openai

from config import OPENAI_KEY

openai.api_key = OPENAI_KEY


async def generate_text_chatgpt4(prompt, name) -> tuple[str, int]:
    logging.info('Отправлен запрос к ChatGPT-4 в OpenAI')
    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[
            {"role": 'user', "content": name + ' пишет:\n' + prompt},
        ]
    )
    text_response = (response['choices'][0]['message']['content'].strip(),
                     response['usage']['total_tokens'])
    logging.info(f'Получен ответ от OpenAI:\n{text_response}')
    return text_response


async def generate_text_chatgpt3(prompt, name) -> tuple[str, int]:
    logging.info('Отправлен запрос к ChatGPT-3 в OpenAI')
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": 'user', "content": name + ' пишет:\n' + prompt},
        ]
    )
    text_response = (response['choices'][0]['message']['content'].strip(),
                     response['usage']['total_tokens'])
    logging.info(f'Получен ответ от OpenAI:\n{text_response}')
    return text_response


async def generate_image_dalle(prompt, n=1, size="1024x1024") -> list[str]:
    logging.info('Отправлен запрос к DALLE в OpenAI')
    response = await openai.Image.acreate(
        prompt=prompt,
        n=n,
        size=size
    )
    urls = []
    for i in response['data']:
        urls.append(i['url'])
    return urls
