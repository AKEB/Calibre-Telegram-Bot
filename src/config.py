"""Модуль для загрузки переменных и настроек"""
# pylint: disable=W0212
# pylint: disable=W0718
import os
import ssl
import logging
import urllib3
from dotenv import load_dotenv


ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Загрузка переменных окружения
load_dotenv()

def get_env_var(name, default=None, split=False, cast=None):
    """Универсальная функция для получения переменных окружения с опциями split и cast."""
    value = os.getenv(name, default)
    if split and value is not None:
        value = value.split(",")
    if cast and value is not None:
        try:
            value = cast(value)
        except Exception:
            value = default
    return value

LOG_LEVEL = get_env_var("LOG_LEVEL", "WARNING").upper()
if LOG_LEVEL not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
    LOG_LEVEL = "WARNING"   # Установка уровня логирования по умолчанию

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=LOG_LEVEL
)
logger = logging.getLogger(__name__)

# Константы

TELEGRAM_BOT_TOKEN = get_env_var("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_ADMIN_USERS = get_env_var("TELEGRAM_ADMIN_USERS", "", split=True)

CALIBRE_DB = get_env_var("CALIBRE_DB", "/books/metadata.db")
BOOKS_DIR = get_env_var("BOOKS_DIR", "/books/")
BOOKS_IMPORT_DIR = get_env_var("BOOKS_IMPORT_DIR", None)
AUTHORIZED_USERS_FILE = get_env_var("AUTHORIZED_USERS_FILE", "authorized_users.txt")

CALIBRE_LIBRARY_URL = get_env_var("CALIBRE_LIBRARY_URL", "")
CALIBRE_LIBRARY_USER = get_env_var("CALIBRE_LIBRARY_USER", "")
CALIBRE_LIBRARY_PASS = get_env_var("CALIBRE_LIBRARY_PASS", "")
CALIBRE_WEB_URL = get_env_var("CALIBRE_WEB_URL", None)

RESULTS_PER_PAGE = get_env_var("RESULTS_PER_PAGE", 5, cast=int)
RANDOM_BOOKS_COUNT = get_env_var("RANDOM_BOOKS_COUNT", 10, cast=int)
BOOKS_LIMIT_COUNT = get_env_var("BOOKS_LIMIT_COUNT", 400, cast=int)
MAX_UPLOAD_SIZE = get_env_var("MAX_UPLOAD_SIZE", 50 * 1024 * 1024, cast=int)

# Константы для ConversationHandler
# pylint: disable=C0301
SEARCH, BOOK_SELECT, FORMAT_SELECT, REQUEST_SEARCH, REQUEST_TITLE, REQUEST_AUTHOR, REQUEST_SERIES, REQUEST_ID, REQUEST_UPLOAD = range(9)

def check_config():
    """Проверка конфигурации и обязательных переменных"""
    logger.debug("check_config() start")
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN не задан!")
        return False

    if not CALIBRE_DB:
        logger.error("CALIBRE_DB не задан!")
        return False

    if not BOOKS_DIR:
        logger.error("BOOKS_DIR не задан!")
        return False

    if not CALIBRE_LIBRARY_URL:
        logger.error("CALIBRE_LIBRARY_URL не задан!")
        return False

    if not CALIBRE_LIBRARY_USER:
        logger.error("CALIBRE_LIBRARY_USER не задан!")
        return False

    if not CALIBRE_LIBRARY_PASS:
        logger.error("CALIBRE_LIBRARY_PASS не задан!")
        return False

    if not os.path.isfile(AUTHORIZED_USERS_FILE):
        with open(AUTHORIZED_USERS_FILE, 'a', encoding='utf-8'):
            pass
    return True


def print_config():
    """Выводит константы в лог"""
    logger.debug("print_config() start")
    logger.info("Telegram Bot configs:")
    logger.info("    TELEGRAM_BOT_TOKEN=%s", TELEGRAM_BOT_TOKEN)
    logger.info("    TELEGRAM_ADMIN_USERS=%s", TELEGRAM_ADMIN_USERS)

    logger.info("    CALIBRE_DB=%s", CALIBRE_DB)
    logger.info("    BOOKS_DIR=%s", BOOKS_DIR)
    logger.info("    BOOKS_IMPORT_DIR=%s", BOOKS_IMPORT_DIR)

    logger.info("    AUTHORIZED_USERS_FILE=%s", AUTHORIZED_USERS_FILE)

    logger.info("    CALIBRE_LIBRARY_URL=%s", CALIBRE_LIBRARY_URL)
    logger.info("    CALIBRE_LIBRARY_USER=%s", CALIBRE_LIBRARY_USER)
    logger.info("    CALIBRE_LIBRARY_PASS=%s", CALIBRE_LIBRARY_PASS)
    logger.info("    CALIBRE_WEB_URL=%s", CALIBRE_WEB_URL)

    logger.info("    RESULTS_PER_PAGE=%s", RESULTS_PER_PAGE)
    logger.info("    RANDOM_BOOKS_COUNT=%s", RANDOM_BOOKS_COUNT)
    logger.info("    BOOKS_LIMIT_COUNT=%s", BOOKS_LIMIT_COUNT)
    logger.info("    MAX_UPLOAD_SIZE=%s", MAX_UPLOAD_SIZE)
