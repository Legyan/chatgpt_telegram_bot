import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message

from constants import NO_ACCESS, NOT_ADMIN
from db import is_admin_user, is_user_in_whitelist


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: dict[str, Any]
    ) -> Any:
        user = event.from_user
        logging.info(
            f'Пользователь {user.id} ({user.username}) написал: {event.text}'
        )
        return await handler(event, data)


class AdminMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: dict[str, Any]
    ) -> Any:
        user = event.from_user
        if not is_admin_user(user.id):
            logging.info(f'У пользователя {user.username} недостаточно прав.')
            await event.answer(NOT_ADMIN)
            return
        return await handler(event, data)


class UserInWhiteListMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: dict[str, Any]
    ) -> Any:
        user = event.from_user
        if not is_user_in_whitelist(user.id):
            logging.info(f'У пользователя {user.username} недостаточно прав.')
            await event.answer(NO_ACCESS)
            return
        return await handler(event, data)
