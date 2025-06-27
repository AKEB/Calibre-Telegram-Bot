"""Показ конкретной книги"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import logger
from download import get_book_formats
from texts import get_text
from auth import Auth

auth = Auth()

def get_book_text(book: dict, user_id) -> str:
    """get_book_text"""
    logger.debug("get_book_text() start")
    lang = auth.get_language(user_id)
    if not book['id']:
        book['id'] = ""
    if not book['author']:
        book['author'] = ""
    if not book['series']:
        book['series'] = ""
    if not book['series_index']:
        book['series_index'] = ""
    if not book['publisher']:
        book['publisher'] = ""
    if not book['text']:
        book['text'] = ""
    if not book['tags']:
        book['tags'] = ""
    publisher_block = get_text(
        "publisher",
        lang,
        publisher=book['publisher']
    ) + "\n" if book['publisher'] else ""
    download_block = get_text("book_download_block", lang)
    text = get_text(
        "book_card", lang,
        title=book['title'],
        author=book['author'],
        series=book['series'],
        series_index=book['series_index'],
        publisher_block=publisher_block,
        id=book['id'],
        tags=book['tags'],
        desc=book['text'][:500],
        download_block=download_block
    )
    return text

def book_selected(book, user_id):
    """book_selected"""
    logger.debug("book_selected() start")
    formats = get_book_formats(book['id'])
    all_formats = ['epub', 'mobi', 'fb2', 'txt', 'azw3']
    for fmt in formats:
        if fmt not in all_formats:
            all_formats.append(fmt)
    keyboard = []
    row = []
    lang = auth.get_language(user_id)
    for fmt in all_formats:
        available = fmt in formats
        emoji = "✅" if available else "🔄"
        row.append(
            InlineKeyboardButton(
                f"{emoji} {fmt.upper()}",
                callback_data=f"format_{fmt}"
            )
        )
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    keyboard.append([
        InlineKeyboardButton(get_text("btn_back", lang), callback_data="back"),
        InlineKeyboardButton(get_text("btn_cancel", lang), callback_data="cancel")
    ])
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = get_book_text(book, user_id)
    return reply_markup, text
