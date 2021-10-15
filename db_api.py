import sqlite3
import config


def update_format_with_args(sql, parameters: dict):
    values = ", ".join([
        f"{item} = ?" for item in parameters
    ])
    sql = sql.replace("XXX", values)
    return sql, tuple(parameters.values())


# Форматирование запроса без аргументов
def get_format_args(sql, parameters: dict):
    sql += " AND ".join([
        f"{item} = ?" for item in parameters
    ])
    return sql, tuple(parameters.values())


def add_user(user_id, is_admin):
    try:
        with sqlite3.connect(config.db_path) as db:
            db.execute("INSERT INTO user_data"
                       "(user_id, is_admin) "
                       "VALUES (?, ?)",
                       [user_id, is_admin])
            db.commit()
    except sqlite3.IntegrityError:
        pass


def update_user(user_id, **kwargs):
    with sqlite3.connect(config.db_path) as db:
        sql = f"UPDATE user_data SET XXX WHERE user_id = {user_id}"
        sql, parameters = update_format_with_args(sql, kwargs)
        db.execute(sql, parameters)
        db.commit()


def get_user(**kwargs):
    with sqlite3.connect(config.db_path) as db:
        sql = "SELECT * FROM user_data WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        return db.execute(sql, parameters).fetchone()


def get_all_users():
    with sqlite3.connect(config.db_path) as db:
        sql = "SELECT * FROM user_data"
        return db.execute(sql).fetchall()


def add_chat(chat_id, title):
    try:
        with sqlite3.connect(config.db_path) as db:
            db.execute("INSERT INTO chat_list"
                       "(chat_id, title) "
                       "VALUES (?, ?)",
                       [chat_id, title])
            db.commit()
    except sqlite3.IntegrityError:
        pass


def update_chat(chat_id, **kwargs):
    with sqlite3.connect(config.db_path) as db:
        sql = f"UPDATE chat_list SET XXX WHERE chat_id = {chat_id}"
        sql, parameters = update_format_with_args(sql, kwargs)
        db.execute(sql, parameters)
        db.commit()


def get_chat(**kwargs):
    with sqlite3.connect(config.db_path) as db:
        sql = "SELECT * FROM chat_list WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        return db.execute(sql, parameters).fetchone()


def get_all_chats():
    with sqlite3.connect(config.db_path) as db:
        sql = "SELECT * FROM chat_list"
        return db.execute(sql).fetchall()


def delete_chat(**kwargs):
    with sqlite3.connect(config.db_path) as db:
        sql = "DELETE FROM chat_list WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        db.execute(sql, parameters)
        db.commit()