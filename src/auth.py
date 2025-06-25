"""Проверка авторизации"""
import os
from config import logger, AUTHORIZED_USERS_FILE, TELEGRAM_ADMIN_USERS

class Auth:
    """Класс для управления пользователями"""
    def __init__(self):
        logger.debug("Auth() start")
        self.authorized_users = self.load_authorized_users()

    def load_authorized_users(self) -> set:
        """Загрузка списка авторизованных пользователей"""
        logger.debug("load_authorized_users() start")

        if not os.path.exists(AUTHORIZED_USERS_FILE):
            return set()
        with open(AUTHORIZED_USERS_FILE, 'r', encoding="utf-8") as f:
            return set(line.strip() for line in f if line.strip())

    def is_authorized(self, user_id) -> bool:
        """Проверка авторизации пользователя"""
        logger.debug("is_authorized() start")
        return str(user_id) in self.authorized_users

    def is_admin(self, user_id) -> bool:
        """Проверка админа"""
        logger.debug("is_admin() start")
        return str(user_id) in TELEGRAM_ADMIN_USERS

    def add_authorized_user(self, user_id) -> bool:
        """Добавляем нового пользователя"""
        logger.debug("add_authorized_user() start")
        try:
            with open(AUTHORIZED_USERS_FILE, 'a', encoding='utf-8') as f:
                f.write(f"{user_id}\n")

            # Обновляем кеш авторизованных пользователей
            self.authorized_users = self.load_authorized_users()

            return True
        except (OSError, IOError) as e:
            logger.error("Ошибка при добавлении пользователя: %s", str(e))
        return False
