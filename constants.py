HELP_TEXT = (
    '/start - Запуск бота. Получить приветственное сообщение и начать '
    'использовать бота для общения с ChatGPT 4 через API OPENAI.\n'
    '/my_tokens - Получить количество использованных пользователем токенов.\n'
    '/add_user - (Только для администраторов) Добавить пользователя '
    'в белый список. '
    'Используйте формат: /add_user <name> <telegram-id>\n'
    '/del_user - (Только для администраторов) Удалить пользователя '
    'из белого списка. '
    'Используйте формат: /del_user <telegram-id>\n'
    '/reset_tokens - (Только для администраторов) Обнулить счетчик токенов '
    'указанного пользователя. Используйте формат: /reset_tokens <telegram-id>\n'
    '/reset_all_tokens - (Только для администраторов) Обнулить счетчики '
    'токенов всех пользователей.\n'
    '/add_admin - (Только для администраторов) Назначить пользователя '
    'администратором. '
    'Используйте формат: /add_admin <telegram-id>\n'
    '/del_admin - (Только для администраторов) Удалить права администратора '
    'у пользователя. '
    'Используйте формат: /del_admin <telegram-id>\n'
    '/users - (Только для администраторов) Получить список всех '
    'пользователей с их данными в виде таблицы.\n'
)
NOT_ADMIN = 'У вас нет прав администратора.'
COMMAND_ERROR = 'При обработке команды возникла ошибка, попробуйте позже.'
NOT_IN_WHITELIST = 'Этого пользователя нет в whitelist.'
NO_ACCESS = 'У вас нет доступа к боту. Обратитесь к администратору.'
