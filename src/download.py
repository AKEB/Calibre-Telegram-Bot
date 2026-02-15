"""Функции для скачивания книги"""
import os
import sqlite3
import tempfile
import subprocess
from telegram.ext import CallbackContext
from telegram.error import TimedOut
from config import logger
from config import CALIBRE_DB, BOOKS_DIR
from texts import get_text
from auth import Auth

auth = Auth()

def get_book_path(book_id, file_format='epub'):
    """Получение пути к файлу книги"""
    logger.debug("get_book_path() start")
    conn = sqlite3.connect(f'file:{CALIBRE_DB}?mode=ro', uri=True)
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT
                   A.path, B.name, B.format
                   FROM books AS A LEFT JOIN data AS B
                   ON A.id=B.book WHERE A.id=?""", (book_id,))
    row = cursor.fetchone()
    conn.close()
    full_path = os.path.join(BOOKS_DIR, row[0], f"{row[1]}.{file_format.lower()}")
    if not os.path.exists(full_path):
        full_path = os.path.join(BOOKS_DIR, row[0], f"{row[1]}.{row[2]}")

    return full_path if os.path.exists(full_path) else None

def get_book_formats(book_id):
    """Получение доступных форматов книги"""
    logger.debug("get_book_formats() start")
    conn = sqlite3.connect(f'file:{CALIBRE_DB}?mode=ro', uri=True)
    cursor = conn.cursor()
    cursor.execute("SELECT format FROM data WHERE book=?", (book_id,))
    formats = [row[0].lower() for row in cursor.fetchall()]
    conn.close()
    return formats

def convert_book(input_path, output_format):
    """Конвертация книги в другой формат"""
    logger.debug("convert_book() start")
    if not input_path or not os.path.exists(input_path):
        return None

    input_format = os.path.splitext(input_path)[1][1:].lower()
    if input_format == output_format.lower():
        return input_path

    with tempfile.NamedTemporaryFile(suffix=f".{output_format}", delete=False) as temp_file:
        output_path = temp_file.name

    try:
        subprocess.run(
            ['ebook-convert', input_path, output_path, '--output-profile', 'tablet'],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return output_path
    except subprocess.CalledProcessError as e:
        logger.error("Ошибка конвертации: %s", str(e))
        return None

async def format_selected(
        book: dict, selected_format: str,
        context: CallbackContext, chat_id: int, user_id: int
    ):
    """format_selected"""
    logger.debug("format_selected() start")
    book_path = get_book_path(book['id'], selected_format)
    lang = auth.get_language(user_id)
    if not book_path or not book_path.endswith(f".{selected_format}"):
        formats = get_book_formats(book['id'])
        if formats:
            original_path = get_book_path(book['id'], formats[0])
            book_path = convert_book(original_path, selected_format)
    if not book_path:
        return get_text("prepare_failed", lang)
    try:
        with open(book_path, 'rb') as f:
            await context.bot.send_document(
                chat_id=chat_id,
                document=f,
                filename=f"{book['title']}.{selected_format}",
                caption=f"📚 {book['title']}\n✍️ {book['author']}",
                write_timeout=300
            )
        return get_text("send_success", lang, fmt=selected_format.upper())
    except TimedOut:
        logger.error("Timeout при отправке файла. Файл слишком большой или медленное соединение.")
        return get_text("send_error", lang)
    except (OSError, IOError) as e:
        logger.error("Ошибка отправки файла: %s", str(e))
        return get_text("send_error", lang)
