import logging
from typing import Union

from aiogram import F, Router, flags
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from prettytable import PrettyTable

import kb
from config import dp
from constants import (COMMAND_ERROR, HELP_TEXT, INVALID_COMMAND_FROM,
                       NOT_IN_WHITELIST)
from db import (add_user, del_user, get_all_users_tokens, get_user_tokens,
                is_user_in_whitelist, reset_all_users_tokens,
                reset_user_tokens, set_admin, update_image_count,
                update_tokens)
from openai_requests import generate_image_dalle, generate_text_chatgpt4
from states import Gen

admins_router = Router()
whitelist_users_router = Router()


@dp.message(Command('start'))
async def start_handler(msg: Message):
    await msg.answer(
        f'Привет {msg.from_user.username}! '
        'Этот бот позволяет общаться с ChatGPT 4 через API OPENAI. '
        'Напишите что нибудь и бот пришлёт вам ответ от ChatGPT.',
        reply_markup=kb.menu
    )


@dp.callback_query(F.data == 'help')
@dp.message(Command('help'))
async def get_tokens_callback(input_obj: Union[CallbackQuery, Message]):
    if isinstance(input_obj, CallbackQuery):
        await input_obj.message.answer(HELP_TEXT)
    else:
        await input_obj.answer(HELP_TEXT)


@dp.message(F.text == 'Меню')
@dp.message(Command('menu'))
async def menu(msg: Message):
    await msg.answer('Главное меню', reply_markup=kb.menu)


@whitelist_users_router.callback_query(F.data == 'my_tokens')
@whitelist_users_router.message(Command('my_tokens'))
async def help_callback(input_obj: Union[CallbackQuery, Message]):
    try:
        tokens = get_user_tokens(input_obj.from_user.id)
        answer = (f'Вы использовали {tokens[0]} токенов '
                  f'и сгенерировали {tokens[1]} изображений.')
    except Exception as error:
        logging.error(error)
        answer = COMMAND_ERROR
    if isinstance(input_obj, CallbackQuery):
        await input_obj.message.answer(answer, reply_markup=kb.exit_kb)
    else:
        await input_obj.answer(answer, reply_markup=kb.exit_kb)


@whitelist_users_router.callback_query(F.data == 'generate_text')
async def input_text_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.text_prompt)
    await clbck.message.edit_text('Введите ваш запрос к ChatGPT:')


@whitelist_users_router.message(Gen.text_prompt)
@flags.chat_action('typing')
async def generate_text(msg: Message):
    mesg = await msg.reply('Ожидание ответа от ChatGPT.')
    name = msg.from_user.username
    message = msg.text
    try:
        gpt_response, tokens = await generate_text_chatgpt4(message, name)
        update_tokens(msg.from_user.id, tokens)
        await mesg.edit_text(gpt_response, disable_web_page_preview=True)
    except Exception as error:
        logging.error(error)
        await msg.edit_text(COMMAND_ERROR, reply_markup=kb.iexit_kb)


@whitelist_users_router.callback_query(F.data == 'generate_image')
async def input_image_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.img_prompt)
    await clbck.message.edit_text('Введите ваш запрос к DALLE:')


@whitelist_users_router.message(Gen.img_prompt)
@flags.chat_action('upload_photo')
async def generate_image(msg: Message):
    mesg = await msg.reply('Ожидание ответа от DALLE.')
    try:
        img = await generate_image_dalle(msg.text)
        update_image_count(msg.from_user.id)
        await mesg.delete()
        await msg.answer_photo(
            photo=img[0], caption=f'Изображение по запросу "{msg.text}"'
        )
    except Exception as error:
        logging.error(error)
        await mesg.answer(COMMAND_ERROR)


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
        x.field_names = ['id', 'name', 'tokens', 'images', 'admin']
        for user in users_list:
            x.add_row(user)
        await msg.answer(
            '```\n' +
            x.get_string(fields=['name', 'tokens', 'images']) +
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
        await msg.reply(gpt_response)
    except Exception as error:
        logging.error(error)
        await msg.reply(COMMAND_ERROR)
