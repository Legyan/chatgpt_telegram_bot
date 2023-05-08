import logging

from aiogram import Router, flags
from aiogram.filters import Command
from aiogram.types import Message
from prettytable import PrettyTable

from config import dp
from constants import (COMMAND_ERROR, HELP_TEXT, INVALID_COMMAND_FROM,
                       NOT_IN_WHITELIST)
from db import (add_user, del_user, get_all_users_tokens, get_user_tokens,
                is_user_in_whitelist, reset_all_users_tokens,
                reset_user_tokens, set_admin, update_tokens)
from openai_requests import generate_text_chatgpt4

admins_router = Router()
whitelist_users_router = Router()


@dp.message(Command('start'))
async def start_handler(msg: Message):
    await msg.answer(
        f'Привет {msg.from_user.username}! '
        'Этот бот позволяет общаться с ChatGPT 4 через API OPENAI. '
        'Напишите что нибудь и бот пришлёт вам ответ от ChatGPT.'
    )


@dp.message(Command('help'))
async def help_message(message: Message):
    await message.reply(HELP_TEXT)


@whitelist_users_router.message(Command('my_tokens'))
async def get_my_tokens_handler(msg: Message):
    try:
        tokens = get_user_tokens(msg.from_user.id)
        await msg.answer(f'Вы использовали {tokens} токенов.')
    except Exception as error:
        logging.error(error)
        await msg.answer(COMMAND_ERROR)


@admins_router.message(Command('add_user'))
async def add_user_handler(msg: Message):
    name = msg.from_user.username
    message = msg.text
    try:
        _, new_user_name, new_user_id = message.split()
    except ValueError:
        logging.warning(INVALID_COMMAND_FROM + name)
        await msg.answer(
            'Неправильный формат ввода нового пользователя. '
            'Введите имя пользователя и его id через пробел.\n'
            '/add_user Name 12345678'
        )
        return
    if is_user_in_whitelist(new_user_id):
        logging.info(
            name + ' (пользователь уже в whitelist), написал:\n' + message
        )
        await msg.answer('Этот пользователь уже в whitelist.')
        return
    try:
        add_user(new_user_id, new_user_name)
        await msg.answer(
            f'Пользователь с именем {new_user_name} и id {new_user_id} '
            'был добавлен в whitelist'
        )
    except Exception as error:
        logging.error(error)
        await msg.answer(COMMAND_ERROR)


@admins_router.message(Command('del_user'))
async def del_user_handler(msg: Message):
    name = msg.from_user.username
    message = msg.text
    try:
        _, del_user_id = message.split()
    except ValueError:
        logging.warning(INVALID_COMMAND_FROM + name)
        await msg.answer(
            'Неправильный формат ввода для удаления '
            'пользователя. Введите id пользователя.\n'
            '/del_user 12345678'
        )
        return
    if not is_user_in_whitelist(del_user_id):
        logging.info(NOT_IN_WHITELIST)
        await msg.answer(NOT_IN_WHITELIST)
        return
    try:
        del_user(del_user_id)
        await msg.answer(
            f'Пользователь с id {del_user_id} был удалён из whitelist')
    except Exception as error:
        logging.error(error)
        await msg.answer(COMMAND_ERROR)


@admins_router.message(Command('reset_tokens'))
async def reset_user_tokens_handler(msg: Message):
    name = msg.from_user.username
    message = msg.text
    try:
        _, user_id = message.split()
    except ValueError:
        logging.warning(INVALID_COMMAND_FROM + name)
        await msg.answer(
            'Неправильный формат ввода для обнуления счётчика '
            'токенов пользователя. Введите id пользователя.\n'
            '/reset_tokens 12345678'
        )
        return
    if not is_user_in_whitelist(user_id):
        logging.warning(INVALID_COMMAND_FROM + name)
        await msg.answer(NOT_IN_WHITELIST)
        return
    try:
        reset_user_tokens(msg.from_user.id)
        await msg.answer('Счётчик токенов для пользователя обнулён.')
    except Exception as error:
        logging.error(error)
        await msg.answer(COMMAND_ERROR)


@admins_router.message(Command('reset_all_tokens'))
async def reset_all_tokens_handler(msg: Message):
    try:
        reset_all_users_tokens()
        await msg.answer('Счётчики токенов всех пользователей обнулены.')
    except Exception as error:
        logging.error(error)
        await msg.answer(COMMAND_ERROR)


@admins_router.message(Command('add_admin'))
async def add_admin_handler(msg: Message):
    name = msg.from_user.username
    message = msg.text
    try:
        _, user_id = message.split()
    except ValueError:
        logging.warning(INVALID_COMMAND_FROM + name)
        await msg.answer(
            'Неправильный формат ввода для добавления '
            'администратора. Введите id пользователя.\n'
            '/add_admin 12345678'
        )
        return
    if not is_user_in_whitelist(user_id):
        logging.warning(NOT_IN_WHITELIST)
        await msg.answer(NOT_IN_WHITELIST)
        return
    try:
        set_admin(user_id, True)
        await msg.answer(
            f'Пользователь с id {user_id} получил права администратора.'
        )
    except Exception as error:
        logging.error(error)
        await msg.answer(COMMAND_ERROR)


@admins_router.message(Command('del_admin'))
async def del_admin_handler(msg: Message):
    name = msg.from_user.username
    message = msg.text
    try:
        _, user_id = message.split()
    except ValueError:
        logging.warning(INVALID_COMMAND_FROM + name)
        await msg.answer(
            'Неправильный формат ввода для '
            'удаления администратора. Введите id пользователя.\n'
            '/del_admin 12345678'
        )
        return
    if not is_user_in_whitelist(user_id):
        logging.warning(NOT_IN_WHITELIST)
        await msg.answer(NOT_IN_WHITELIST)
        return
    try:
        set_admin(user_id, False)
        await msg.answer(
            f'Пользователь с id {user_id} больше не имеет прав администратора.'
        )
    except Exception as error:
        logging.error(error)
        await msg.answer(COMMAND_ERROR)


@admins_router.message(Command('users'))
async def all_users_handler(msg: Message):
    try:
        users_list = get_all_users_tokens()
        x = PrettyTable()
        x.field_names = ['id', 'name', 'tokens', 'admin']
        for user in users_list:
            x.add_row(user)
        await msg.answer(
            '```\n' +
            x.get_string(fields=['id', 'name', 'tokens']) +
            '\n```',
            parse_mode='MarkdownV2'
        )
    except Exception as error:
        logging.error(error)
        await msg.answer(COMMAND_ERROR)


@whitelist_users_router.message()
@flags.chat_action('typing')
async def message_handler(msg: Message):
    name = msg.from_user.username
    message = msg.text
    try:
        gpt_response, tokens = await generate_text_chatgpt4(message, name)
        update_tokens(msg.from_user.id, tokens)
        await msg.answer(gpt_response)
    except Exception as error:
        logging.error(error)
        await msg.answer(COMMAND_ERROR)
