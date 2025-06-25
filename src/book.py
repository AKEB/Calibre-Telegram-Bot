"""Отображение конкретной книги"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import logger
from download import get_book_formats

def get_book_text(book: dict) -> str:
    """get_book_text"""
    logger.debug("get_book_text() start")

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

    text = ""
    text += f"📚 Выбрана: <b>{book['title']}</b>\n"
    text += f"✍️ Автор: {book['author']}\n"
    text += f"📖 Серия: {book['series']} [{book['series_index']}]\n"
    if book['publisher']:
        text += f"Издатель: {book['publisher']}\n"
    text += f"Идентификатор: {book['id']}\n"
    text += f"Жанр: {book['tags']}\n"
    text += f"Описание: <blockquote>{book['text'][:500]}</blockquote>\n"

    text += "\nВыберите формат для скачивания:\n"
    text += "✅ - доступен сразу\n"
    text += "🔄 - будет сконвертирован из доступного формата"
    return text

def book_selected(book):
    """book_selected"""
    logger.debug("book_selected() start")
    formats = get_book_formats(book['id'])
    all_formats = ['epub', 'mobi', 'fb2', 'txt', 'azw3']

    for fmt in formats:
        if fmt not in all_formats:
            all_formats.append(fmt)

    keyboard = []
    row = []
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
        InlineKeyboardButton("⬅️ Назад", callback_data="back"),
        InlineKeyboardButton("❌ Отмена", callback_data="cancel")
    ])

    reply_markup = InlineKeyboardMarkup(keyboard)

    text = get_book_text(book)

    return reply_markup, text
