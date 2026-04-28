class User:
    def __init__(self, user_info: dict, db):
        self.anonymous_id = user_info["anonymous_id"]
        self.user_id = user_info["user_id"]
        self.user_username = user_info["user_username"]
        self.chat_id = user_info["chat_id"]
        self.name = user_info["name"]
        self.description = user_info["description"]
        self.status = user_info["status"]
        self.likes = user_info["likes"]
        self.dislikes = user_info["dislikes"]
        self.partner_id = user_info["partner_id"]

        self.db = db  # Сохраняем ссылку на объект базы данных

    def is_status(self, status: str) -> bool:
        return self.status == status

    def get_partner(self) -> "User":
        if not self.partner_id or self.partner_id == 0:
            return None
        # Возвращаем объект партнера, вызывая асинхронный метод БД
        return self.db.get_user(self.partner_id)

    def update_status(self, new_status: str):
        # Пример метода, который сам обновляет себя в базе
        self.db.change_status(self.user_id, new_status)
        self.status = new_status