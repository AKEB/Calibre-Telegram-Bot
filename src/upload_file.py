"""Функции для загрузки книги в Calibre"""
import os
import tempfile
import subprocess
from subprocess import SubprocessError, TimeoutExpired, CalledProcessError
import requests
from requests.exceptions import RequestException
from telegram import Update
from telegram.constants import ChatAction
from telegram.error import TelegramError
from telegram.ext import CallbackContext
from config import (
    logger, MAX_UPLOAD_SIZE,
    CALIBRE_LIBRARY_URL, CALIBRE_LIBRARY_USER,
    CALIBRE_LIBRARY_PASS
)
from texts import get_text
from auth import Auth

auth = Auth()

async def handle_document_upload(update: Update, context: CallbackContext) -> None:
    """Обработка загрузки книги из документа"""
    logger.debug("handle_document_upload() start")
    document = update.message.document

    if document.file_size > MAX_UPLOAD_SIZE:
        await (update.message if update.message else update.edited_message).reply_text(
            get_text(
                "file_too_large",
                auth.get_language(update.effective_user.id), max_mb=MAX_UPLOAD_SIZE//1024//1024
            )
        )
        return

    # Проверяем допустимые форматы
    valid_formats = ['epub', 'fb2', 'mobi', 'pdf', 'azw', 'azw3', 'txt']
    file_ext = document.file_name.split('.')[-1].lower() if document.file_name else ''
    if file_ext not in valid_formats:
        await (update.message if update.message else update.edited_message).reply_text(
            get_text(
                "unsupported_format",
                auth.get_language(update.effective_user.id), formats=', '.join(valid_formats)
            )
        )
        return

    # Показываем статус "загружаем файл"
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.UPLOAD_DOCUMENT
    )

    try:
        # Скачиваем файл
        file = await context.bot.get_file(document.file_id)
        temp_dir = tempfile.mkdtemp()
        local_path = os.path.join(temp_dir, document.file_name or f"book.{file_ext}")

        await file.download_to_drive(local_path)

        # Добавляем книгу в Calibre
        await add_book_to_calibre(update, context, local_path)

    except TelegramError as e:
        logger.error("Ошибка Telegram при загрузке книги: %s", str(e))
        await (update.message if update.message else update.edited_message
              ).reply_text(
                  get_text(
                      "telegram_error",
                      auth.get_language(update.effective_user.id), error=str(e)
                  )
              )
    except (OSError, IOError) as e:
        logger.error("Ошибка файловой системы при загрузке книги: %s", str(e))
        await (update.message if update.message else update.edited_message
               ).reply_text(
                   get_text("fs_error", auth.get_language(update.effective_user.id), error=str(e))
                )
    finally:
        # Удаляем временные файлы
        if 'local_path' in locals() and os.path.exists(local_path):
            os.remove(local_path)
        if 'temp_dir' in locals() and os.path.exists(temp_dir):
            os.rmdir(temp_dir)

async def handle_url_upload(update: Update, context: CallbackContext, url: str) -> None:
    """Обработка загрузки книги по URL"""
    logger.debug("handle_url_upload() start")
    # Показываем статус "печатает"
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING
    )

    try:
        # Скачиваем файл по URL
        temp_dir = tempfile.mkdtemp()
        local_path = os.path.join(temp_dir, os.path.basename(url))

        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()

        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        # Добавляем книгу в Calibre
        await add_book_to_calibre(update, context, local_path)

    except RequestException as e:
        logger.error("Ошибка при загрузке книги по URL: %s", str(e))
        await (update.message if update.message else update.edited_message
               ).reply_text(
                   get_text(
                       "url_error",
                       auth.get_language(update.effective_user.id), error=str(e)
                   )
               )
    except (OSError, IOError) as e:
        logger.error("Ошибка файловой системы при загрузке книги: %s", str(e))
        await (update.message if update.message else update.edited_message
               ).reply_text(
                   get_text(
                       "fs_error", auth.get_language(update.effective_user.id), error=str(e)
                   )
               )
    finally:
        # Удаляем временные файлы
        if 'local_path' in locals() and os.path.exists(local_path):
            os.remove(local_path)
        if 'temp_dir' in locals() and os.path.exists(temp_dir):
            os.rmdir(temp_dir)

async def add_book_to_calibre(update: Update, context: CallbackContext, file_path: str) -> None:
    """Добавление книги в Calibre"""
    logger.debug("add_book_to_calibre() start")
    # Показываем статус "добавляем в библиотеку"
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING
    )

    try:
        cmd = [
            'calibredb', 'add',
            '--automerge', 'ignore',
            '--with-library', CALIBRE_LIBRARY_URL,
            '--username', CALIBRE_LIBRARY_USER,
            '--password', CALIBRE_LIBRARY_PASS,
            file_path
        ]

        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
            timeout=600  # 10 минут на загрузку
        )

        if result.returncode == 0:
            # Пытаемся извлечь ID добавленной книги из вывода
            book_id = None
            for line in result.stdout.split('\n'):
                if 'Added book id' in line:
                    book_id = line.split()[-1]
                    break

            if book_id:
                message = get_text(
                    "add_success_calibre",
                    auth.get_language(update.effective_user.id), book_id=book_id
                )
            else:
                message = get_text(
                    "add_success_calibre_noid",
                    auth.get_language(update.effective_user.id), stdout=result.stdout
                )
            await (update.message if update.message else update.edited_message).reply_text(message)
        else:
            error_msg = result.stderr or "Неизвестная ошибка"
            await (update.message if update.message else update.edited_message
                   ).reply_text(
                       get_text(
                           "add_error_calibre",
                           auth.get_language(update.effective_user.id), error=error_msg
                        )
                    )
    except TimeoutExpired:
        await (update.message if update.message else update.edited_message
               ).reply_text(get_text(
                   "timeout_calibre", auth.get_language(update.effective_user.id)
                ))
    except (SubprocessError, CalledProcessError) as e:
        logger.error("Ошибка subprocess при добавлении книги в Calibre: %s", str(e))
        await (update.message if update.message else update.edited_message
               ).reply_text(get_text(
                   "add_error_calibre", auth.get_language(update.effective_user.id), error=str(e)
                ))
    except (OSError, IOError) as e:
        logger.error("Ошибка файловой системы при добавлении книги: %s", str(e))
        await (update.message if update.message else update.edited_message
               ).reply_text(get_text(
                   "fs_error", auth.get_language(update.effective_user.id), error=str(e)
                ))
