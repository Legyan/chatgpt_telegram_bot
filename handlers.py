import logging

from aiogram import flags
from aiogram.types import Message
from aiogram.filters import Command

from config import dp
from db import (is_user_in_whitelist, update_tokens, is_admin_user,
                add_user, del_user, get_user_tokens, reset_user_tokens,
                reset_all_users_tokens, set_admin, get_all_users_tokens)
from openai_requests import generate_text_chatgpt4


@dp.message(Command('start'))
async def start_handler(msg: Message):
    await msg.answer(f'Привет {msg.from_user.username}! '
                     f'Этот бот позволяет общаться с ChatGPT 4 через API OPENAI. '
                     f'Напишите что нибудь и бот пришлёт вам ответ от ChatGPT.')


@dp.message(Command('add_user'))
async def add_user_handler(msg: Message):
    name = msg.from_user.username
    message = msg.text
    if not is_admin_user(msg.from_user.id):
        logging.warning(name + ' (не admin), написал:\n' + message)
        await msg.answer('У вас нет прав администратора.')
        return
    try:
        _, new_user_name, new_user_id = message.split()
    except ValueError:
        logging.warning(name + ' (неправильный формат ввода), написал:\n' + message)
        await msg.answer('Неправильный формат ввода нового пользователя. '
                         'Введите имя пользователя и его id через пробел.\n'
                         '/add_user Name 12345678')
        return
    if is_user_in_whitelist(new_user_id):
        logging.info(name + ' (пользователь уже в whitelist), написал:\n' + message)
        await msg.answer('Этот пользователь уже в whitelist.')
        return
    try:
        add_user(new_user_id, new_user_name)
        await msg.answer(f'Пользователь с именем {new_user_name} и id {new_user_id} '
                         f'был добавлен в whitelist')
    except Exception as error:
        logging.error(error)
        await msg.answer(f'При добавлении пользователя возникла ошибка, попробуйте позже.')


@dp.message(Command('del_user'))
async def del_user_handler(msg: Message):
    name = msg.from_user.username
    message = msg.text
    if not is_admin_user(msg.from_user.id):
        logging.warning(name + ' (не admin), написал:\n' + message)
        await msg.answer('У вас нет прав администратора.')
        return
    try:
        _, del_user_id = message.split()
    except ValueError:
        logging.warning(name + ' (неправильный формат ввода), написал:\n' + message)
        await msg.answer('Неправильный формат ввода для удаления пользователя. '
                         'Введите id пользователя.\n'
                         '/del_user 12345678')
        return
    if not is_user_in_whitelist(del_user_id):
        logging.info(name + ' (пользователя нет в whitelist), написал:\n' + message)
        await msg.answer('Пользователя с введённым id нет whitelist.')
        return
    try:
        del_user(del_user_id)
        await msg.answer(f'Пользователь с id {del_user_id} '
                         f'был удалён из whitelist')
    except Exception as error:
        logging.error(error)
        await msg.answer(f'При удалении пользователя возникла ошибка, попробуйте позже.')


@dp.message(Command('my_tokens'))
async def get_my_tokens_handler(msg: Message):
    name = msg.from_user.username
    message = msg.text
    if not is_user_in_whitelist(msg.from_user.id):
        logging.warning(name + ' (нет в whitelist), написал:\n' + message)
        await msg.answer('У вас нет доступа к боту. Обратитесь к администратору.')
        return
    try:
        tokens = get_user_tokens(msg.from_user.id)
        await msg.answer(f'Вы использовали {tokens} токенов')
    except Exception as error:
        logging.error(error)
        await msg.answer(f'При получении информации произошла ошибка, попробуйте позже.')


@dp.message(Command('reset_tokens'))
async def reset_user_tokens_handler(msg: Message):
    name = msg.from_user.username
    message = msg.text
    if not is_admin_user(msg.from_user.id):
        logging.warning(name + ' (не admin), написал:\n' + message)
        await msg.answer('У вас нет прав администратора.')
        return
    try:
        _, user_id = message.split()
    except ValueError:
        logging.warning(name + ' (неправильный формат ввода), написал:\n' + message)
        await msg.answer('Неправильный формат ввода для обнуления счётчика токенов пользователя. '
                         'Введите id пользователя.\n'
                         '/reset_tokens 12345678')
        return
    if not is_user_in_whitelist(msg.from_user.id):
        logging.warning(name + ' (нет в whitelist), написал:\n' + message)
        await msg.answer('У вас нет доступа к боту. Обратитесь к администратору.')
        return
    try:
        reset_user_tokens(msg.from_user.id)
        await msg.answer(f'Счётчик токенов для пользователя обнулён.')
    except Exception as error:
        logging.error(error)
        await msg.answer(f'При обнулении счётчика произошла ошибка, попробуйте позже.')


@dp.message(Command('reset_all_tokens'))
async def reset_all_tokens_handler(msg: Message):
    name = msg.from_user.username
    message = msg.text
    if not is_admin_user(msg.from_user.id):
        logging.warning(name + ' (не admin), написал:\n' + message)
        await msg.answer('У вас нет прав администратора.')
        return
    try:
        reset_all_users_tokens()
        await msg.answer(f'Счётчики токенов всех пользователей обнулены.')
    except Exception as error:
        logging.error(error)
        await msg.answer(f'При обнулении счётчиков произошла ошибка, попробуйте позже.')


@dp.message(Command('add_admin'))
async def add_admin_handler(msg: Message):
    name = msg.from_user.username
    message = msg.text
    if not is_admin_user(msg.from_user.id):
        logging.warning(name + ' (не admin), написал:\n' + message)
        await msg.answer('У вас нет прав администратора.')
        return
    try:
        _, user_id = message.split()
    except ValueError:
        logging.warning(name + ' (неправильный формат ввода), написал:\n' + message)
        await msg.answer('Неправильный формат ввода для добавления администратора. '
                         'Введите id пользователя.\n'
                         '/add_admin 12345678')
        return
    if not is_user_in_whitelist(user_id):
        logging.warning(name + ' (админ. права для пользователя не в whitelist), написал:\n' + message)
        await msg.answer('Этого пользователя нет в whitelist.')
        return
    try:
        set_admin(user_id, True)
        await msg.answer(f'Пользователь с id {user_id} получил права администратора.')
    except Exception as error:
        logging.error(error)
        await msg.answer(f'При попытке добавления администратора возникла ошибка, попробуйте позже.')


@dp.message(Command('del_admin'))
async def del_admin_handler(msg: Message):
    name = msg.from_user.username
    message = msg.text
    if not is_admin_user(msg.from_user.id):
        logging.warning(name + ' (не admin), написал:\n' + message)
        await msg.answer('У вас нет прав администратора.')
        return
    try:
        _, user_id = message.split()
    except ValueError:
        logging.warning(name + ' (неправильный формат ввода), написал:\n' + message)
        await msg.answer('Неправильный формат ввода для удаления администратора. '
                         'Введите id пользователя.\n'
                         '/del_admin 12345678')
        return
    if not is_user_in_whitelist(user_id):
        logging.warning(name + ' (удаление админ. прав для пользователя не в whitelist), написал:\n' + message)
        await msg.answer('Этого пользователя нет в whitelist.')
        return
    try:
        set_admin(user_id, False)
        await msg.answer(f'Пользователь с id {user_id} больше не имеет прав администратора.')
    except Exception as error:
        logging.error(error)
        await msg.answer(f'При попытке удаленияц администратора возникла ошибка, попробуйте позже.')


@dp.message(Command('users'))
async def all_users_handler(msg: Message):
    name = msg.from_user.username
    message = msg.text
    if not is_admin_user(msg.from_user.id):
        logging.warning(name + ' (не admin), написал:\n' + message)
        await msg.answer('У вас нет прав администратора.')
        return
    try:
        users_list = get_all_users_tokens()
        answer = ''
        for user in users_list:
            for p in user:
                answer += str(p) + ' '
            answer += '\n'
        await msg.answer(answer)
    except Exception as error:
        logging.error(error)
        await msg.answer(f'При попытке удаленияц администратора возникла ошибка, попробуйте позже.')


@dp.message()
@flags.chat_action('typing')
async def message_handler(msg: Message):
    name = msg.from_user.username
    message = msg.text
    if not is_user_in_whitelist(msg.from_user.id):
        logging.warning(name + ' (нет в whitelist), написал:\n' + message)
        await msg.answer('У вас нет доступа к боту. Обратитесь к администратору.')
        return
    logging.info(name + ' написал:\n' + message)
    try:
        gpt_response, tokens = await generate_text_chatgpt4(message, name)
        update_tokens(msg.from_user.id, tokens)
        await msg.answer(gpt_response)
    except Exception as error:
        logging.error(f'Error: {error}')
        await msg.answer('Запрос к OpenAI не получил ответа, попробуйте позже.')

