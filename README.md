# ChatGPT telegram-bot

Телеграм-бот, который и спользует GPT-4 от OpenAI для ответа на сообщения пользователей. 
Бот логирует сообщения пользователей и ответы от OpenAI, сохраняя логи в файле logs/chat_gpt_bot.log.

## Стек технологий 

![](https://img.shields.io/badge/Python-3.10-black?style=flat&logo=python) 
![](https://img.shields.io/badge/python_telegram_bot-13.7-black?style=flat&logo=telegram)
![](https://img.shields.io/badge/Openai-0.27.0-black?style=flat&logo=openai)

## Запуск проекта

1. Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/legyan/chatgpt-telegram-bot.git
```

```
cd chatgpt-telegram-bot
```

2. Установить зависимости с помощью [Poetry](https://python-poetry.org/docs/):

```
poetry install
```

3. Создать в корневой директории файл .env и заполнить его данными:

```
touch .env && nano .env
```

```
BOT_TOKEN=<YOUR_BOT_TOKEN>
OPENAI_API_KEY=<YOUR_OPENAPI_KEY>
```

4. Запустить бота с помощью Poetry:

```
poetry run python main.py
```
