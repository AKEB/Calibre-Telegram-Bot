#!/usr/bin/env python3
"""Бот для поиска и скачивания книг с сайта"""
import sys
from telegram.ext import Application
from config import logger, check_config, print_config, TELEGRAM_BOT_TOKEN

from database import check_db_permissions
from handlers import setup_handlers

def main() -> None:
    """Запуск бота"""
    logger.debug("main() start")

    if not check_config():
        logger.critical("Проблемы с конфигурацией. Проверьте настройки.")
        sys.exit(1)

    print_config()

    if not check_db_permissions():
        logger.critical("Проблемы с доступом к базе данных. Проверьте права доступа.")
        sys.exit(1)

    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    setup_handlers(application)

    application.run_polling()

if __name__ == '__main__':
    main()
