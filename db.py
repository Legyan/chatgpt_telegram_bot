import sqlite3

from config import ADMINS_ACCOUNTS


def create_database():
    conn = sqlite3.connect('users_tokens.db')
    c = conn.cursor()

    c.execute(
        '''CREATE TABLE IF NOT EXISTS users (
           id INTEGER PRIMARY KEY,
           name varchar(20),
           tokens INTEGER,
           is_admin bool
           )''')

    add_column_if_not_exists(
        c, "users", "generated_images", "INTEGER DEFAULT 0"
    )

    for admin in ADMINS_ACCOUNTS.split(';'):
        user_id, name = admin.split(',')
        if not is_user_in_whitelist(int(user_id)):
            add_user(int(user_id), name, True)

    conn.commit()
    conn.close()


def add_column_if_not_exists(
        cursor, table_name, column_name, column_definition
):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    if not any(column[1] == column_name for column in columns):
        cursor.execute(
            f"ALTER TABLE {table_name} "
            f"ADD COLUMN {column_name} {column_definition}"
        )


def add_user(user_id, name, is_admin=False):
    conn = sqlite3.connect('users_tokens.db')
    c = conn.cursor()
    c.execute(
        'INSERT OR IGNORE INTO '
        'users (id, name, tokens, generated_images, is_admin) '
        'VALUES (?, ?, 0, 0, ?)', (user_id, name, is_admin)
    )
    conn.commit()
    conn.close()


def set_admin(user_id, is_admin):
    conn = sqlite3.connect('users_tokens.db')
    c = conn.cursor()
    c.execute(
        'UPDATE users SET is_admin = ? WHERE id = ?', (is_admin, user_id)
    )
    conn.commit()
    conn.close()


def del_user(user_id):
    conn = sqlite3.connect('users_tokens.db')
    c = conn.cursor()
    c.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()


def update_tokens(user_id, tokens):
    conn = sqlite3.connect('users_tokens.db')
    c = conn.cursor()
    c.execute(
        'UPDATE users SET tokens = tokens + ? WHERE id = ?', (tokens, user_id)
    )
    conn.commit()
    conn.close()


def update_image_count(user_id):
    conn = sqlite3.connect('users_tokens.db')
    c = conn.cursor()
    c.execute(
        'UPDATE users '
        'SET generated_images = generated_images + 1 '
        'WHERE id = ?', (user_id,)
    )
    conn.commit()
    conn.close()


def get_user_tokens(user_id):
    conn = sqlite3.connect('users_tokens.db')
    c = conn.cursor()
    c.execute(
        'SELECT tokens, generated_images FROM users WHERE id = ?', (user_id,)
    )
    tokens = c.fetchone()
    conn.close()
    return tokens


def reset_user_tokens(user_id):
    conn = sqlite3.connect('users_tokens.db')
    c = conn.cursor()
    c.execute(
        'UPDATE users '
        'SET tokens = 0, generated_images = 0 '
        'WHERE id = ?', (user_id,)
    )
    conn.commit()
    conn.close()


def reset_all_users_tokens():
    conn = sqlite3.connect('users_tokens.db')
    c = conn.cursor()
    c.execute('UPDATE users SET tokens = 0, generated_images = 0')
    conn.commit()
    conn.close()


def get_all_users_tokens():
    conn = sqlite3.connect('users_tokens.db')
    c = conn.cursor()
    c.execute('SELECT id, name, tokens, generated_images, is_admin FROM users')
    users_tokens = c.fetchall()
    conn.close()
    return users_tokens


def is_user_in_whitelist(user_id):
    conn = sqlite3.connect('users_tokens.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    conn.close()
    return user is not None


def is_admin_user(user_id):
    conn = sqlite3.connect('users_tokens.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id = ? AND is_admin = 1', (user_id,))
    user = c.fetchone()
    conn.close()
    return user is not None


create_database()
