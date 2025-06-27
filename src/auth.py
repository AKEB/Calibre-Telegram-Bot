"""Проверка авторизации"""
import os
from config import logger, AUTHORIZED_USERS_FILE, TELEGRAM_ADMIN_USERS

class Auth:
    """Класс для управления пользователями"""
    def __init__(self):
        logger.debug("Auth() start")
        self.authorized_users = self.load_authorized_users()

    def load_authorized_users(self) -> dict:
        """Загрузка списка авторизованных пользователей с языком"""
        logger.debug("load_authorized_users() start")
        users = {}
        if not os.path.exists(AUTHORIZED_USERS_FILE):
            return users
        with open(AUTHORIZED_USERS_FILE, 'r', encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',')
                user_id = parts[0]
                lang = parts[1] if len(parts) > 1 else 'ru'
                users[user_id] = lang
        return users

    def is_authorized(self, user_id) -> bool:
        """Проверка авторизации пользователя"""
        logger.debug("is_authorized() start")
        return str(user_id) in self.authorized_users

    def get_language(self, user_id) -> str:
        """Получить язык пользователя (по умолчанию ru)"""
        return self.authorized_users.get(str(user_id), 'ru')

    def set_language(self, user_id, lang) -> None:
        """Установить язык пользователя и сохранить в файл"""
        user_id = str(user_id)
        self.authorized_users[user_id] = lang
        # Перезаписываем файл полностью
        try:
            with open(AUTHORIZED_USERS_FILE, 'w', encoding='utf-8') as f:
                for uid, lng in self.authorized_users.items():
                    f.write(f"{uid},{lng}\n")
        except (OSError, IOError) as e:
            logger.error("Ошибка при сохранении языка пользователя: %s", str(e))

    def is_admin(self, user_id) -> bool:
        """Проверка админа"""
        logger.debug("is_admin() start")
        return str(user_id) in TELEGRAM_ADMIN_USERS

    def add_authorized_user(self, user_id) -> bool:
        """Добавляем нового пользователя (по умолчанию язык ru)"""
        logger.debug("add_authorized_user() start")
        try:
            user_id = str(user_id)
            if user_id not in self.authorized_users:
                self.authorized_users[user_id] = 'ru'
                with open(AUTHORIZED_USERS_FILE, 'a', encoding='utf-8') as f:
                    f.write(f"{user_id},ru\n")
            # Обновляем кеш авторизованных пользователей
            self.authorized_users = self.load_authorized_users()
            return True
        except (OSError, IOError) as e:
            logger.error("Ошибка при добавлении пользователя: %s", str(e))
        return False
