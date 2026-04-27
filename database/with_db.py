import sqlite3
import os
import config
#мои модули
from models import User

class Database:
    def __init__(self):
        current_dir = os.path.dirname(__file__)
        # config.json теперь точно найдется благодаря os.path
        name_db = config.load_json()["db"]
        self.db_path = os.path.abspath(os.path.join(current_dir, name_db))

    def query(self, sql: str, params: tuple = (), is_select: bool = False) -> list[dict] | None:
        try:
            with sqlite3.connect(self.db_path, check_same_thread=False) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(sql, params)
                if is_select:
                    return [dict(row) for row in cursor.fetchall()]
                conn.commit()
        except Exception as e:
            # Если что-то упадет, ты увидишь точный текст ошибки в консоли сервера
            print(f"Ошибка БД: {e} | SQL: {sql} | Params: {params}")
        return None

    def create_table(self):
        self.query("""
            CREATE TABLE IF NOT EXISTS users (
                anonymous_id INTEGER PRIMARY KEY
                user_id INTEGER,
                user_username TEXT, 
                chat_id INTEGER, 
                name TEXT DEFAULT 'Аноним', 
                description TEXT DEFAULT 'Это новый Аноним', 
                status TEXT DEFAULT 'idle',
                likes INTEGER DEFAULT 0, 
                dislikes INTEGER DEFAULT 0,
                partner_id INTEGER DEFAULT 0
            )
        """)

    def get_user(self, user_id: int) -> User | None:
        result = self.query("SELECT rowid, * FROM users WHERE user_id = ?", (user_id,), is_select=True)
        if result:
            return User(result[0], self)
        return None

    def add_user(self, user_id: int, chat_id: int, username: str) -> dict:
        # ИСПРАВЛЕНИЕ 1: Добавил третий знак вопроса (было 2, а колонок 3)
        self.query(
            "INSERT OR IGNORE INTO users (user_id, chat_id, user_username) VALUES (?, ?, ?)",
            (user_id, chat_id, username)
        )
        return self.get_user(user_id)

    def unification_of_users(self, user_id: int, partner_id: int):
        for pid, uid in [(partner_id, user_id), (user_id, partner_id)]:
            # ИСПРАВЛЕНИЕ 2: Обернул 'chatting' в кавычки, чтобы SQL не думал, что это имя колонки
            self.query("UPDATE users SET status = 'chatting', partner_id = ? WHERE user_id = ?", (pid, uid))

    def change_status(self, user_id: int, status: str):
        self.query("UPDATE users SET status = ? WHERE user_id = ?", (status, user_id))

    def add_likes_dislikes(self, user_id: int, type_l: str, quantity: int = 1):
        # ИСПРАВЛЕНИЕ 3: Исправил логику. Мы передаем partner_id, чтобы начислить лайк ПАРТНЕРУ
        if type_l == "likes":
            self.query("UPDATE users SET likes = likes + ? WHERE user_id = ?", (quantity, user_id))
        elif type_l == "dislikes":
            self.query("UPDATE users SET dislikes = dislikes + ? WHERE user_id = ?", (quantity, user_id))

    def get_user_storage(self, user_id: int, user_chat_id: int, username: str) -> dict:
        return self.add_user(user_id, user_chat_id, username)
