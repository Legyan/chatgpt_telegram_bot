# ChatGPT telegram-bot

## Описание

Телеграм-бот, который использует GPT-4 от OpenAI для ответа на сообщения пользователей. 
Бот доступен только пользователям из белого списка, управление списком могут осуществлять пользователи с правами администратора. 
Для каждого пользователя в списке ведётся подсчёт токенов, потраченных этим пользователем на общение с ChatGPT.
Бот логирует сообщения пользователей и ответы от API OpenAI, сохраняя логи в файле logs/chat_gpt_bot.log.

### Команды

- **/start** - Запуск бота. Получить приветственное сообщение и начать использовать бота для общения с ChatGPT.


- **/help** - Получить справку о доступных командах бота.


- **/my_tokens** - Получить количество использованных пользователем токенов.

#### Команды для администраторов

- **/add_user** - Добавить пользователя в белый список. Используйте формат: ```/add_user <name> <telegram-id>```


- **/del_user** - Удалить пользователя из белого списка. Используйте формат: ```/del_user <telegram-id>```


- **/reset_tokens** - Обнулить счетчик токенов указанного пользователя. Используйте формат: ```/reset_tokens <telegram-id>```


- **/reset_all_tokens** - Обнулить счетчики токенов всех пользователей.


- **/add_admin** - Назначить пользователя администратором. Используйте формат: ```/add_admin <telegram-id>```


- **/del_admin** - Удалить права администратора у пользователя. Используйте формат: ```/del_admin <telegram-id>```


- **/users** - Получить список всех пользователей с их данными в виде таблицы.

## Стек технологий 

![](https://img.shields.io/badge/Python-3.10-black?style=flat&logo=python) 
![](https://img.shields.io/badge/aiogram-3.0.0b7-black?style=flat&logo=telegram)
![](https://img.shields.io/badge/Openai-0.27.0-black?style=flat&logo=openai)
![](https://img.shields.io/badge/SQLite-3.7.15-black?style=flat&logo=sqlite)

## Запуск проекта

1. Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/legyan/chatgpt_telegram_bot.git
```

```
cd chatgpt_telegram_bot
```

2. Установить зависимости с помощью [Poetry](https://python-poetry.org/docs/):

```
poetry install
```

3. Создать в корневой директории файл .env и заполнить его данными:

```
nano .env
```

```
ADMINS_ACCOUNTS=<FIRST_ADMIN_ID>,<FIRST_ADMIN_NAME>
BOT_TOKEN=<YOUR_BOT_TOKEN>
OPENAI_API_KEY=<YOUR_OPENAPI_KEY>
```

Если необходимо при создании базы добавлять в неё более одного администратора, то необходимо указать их telegram-id и имена далее в переменной ```ADMINS_ACCOUNTS```, 
разделяя данные отдельных администраторов с помощью ```;```, как в примере в файле .env.example. 

4. Запустить бота с помощью Poetry:

```
poetry run python main.py
```
