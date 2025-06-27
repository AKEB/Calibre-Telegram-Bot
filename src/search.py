"""Функции для отображения книг"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ChatAction
from telegram.error import TelegramError
from telegram.ext import CallbackContext
from config import logger, RESULTS_PER_PAGE, BOOK_SELECT
from reset import reset_search
from database import search_books
from texts import get_text
from auth import Auth

auth = Auth()

def get_file_size(size: int) -> str:
    """Преобразование размера файла в человекочитаемый формат"""
    logger.debug("get_file_size() start")
    if size < 1024:
        return f"{size}B"
    elif size < 1024 * 1024:
        return f"{size / 1024:.2f}KB"
    elif size < 1024 * 1024 * 1024:
        return f"{size / (1024 * 1024):.2f}MB"
    else:
        return f"{size / (1024 * 1024 * 1024):.2f}GB"


def get_books_list_text(page_books, start_idx, lang) -> str:
    """get_books_list_text"""
    logger.debug("get_books_list_text() start")
    books_text = ""
    for i, book in enumerate(page_books, start=start_idx+1):
        books_text += f"{i}. 📚 <b>{book['title']}</b>"
        if book['languages']:
            books_text += f" (<i>{book['languages']}</i>)"
        books_text += "\n"
        books_text += f"\t\t\t\t✍️ <i>{book['author']}</i>\n"
        if book['id']:
            books_text += "\t\t\t\t" + get_text("search_id", lang, id=book['id'])
        if book['publisher']:
            books_text += " \t\t" + get_text("search_publisher", lang, publisher=book['publisher'])
        if book['size']:
            books_text += " \t\t" + get_text("search_size", lang, size=get_file_size(book['size']))
        books_text += "\n"
        if book['series']:
            books_text += "\t\t\t\t" + get_text(
                "search_series", lang,
                series=book['series'],
                series_index=book['series_index']
            ) + "\n"
        if book['tags']:
            books_text += "\t\t\t\t" + get_text("search_genre", lang, tags=book['tags']) + "\n"
        books_text += "\n"
    return books_text

def get_books_search_message_with_buttons(books, current_page, lang=None):
    """get_books_search_message_with_buttons"""
    logger.debug("get_books_search_message_with_buttons() start")
    total_books = len(books)
    total_pages = (total_books + RESULTS_PER_PAGE - 1) // RESULTS_PER_PAGE
    start_idx = current_page * RESULTS_PER_PAGE
    end_idx = min(start_idx + RESULTS_PER_PAGE, total_books)
    lang = lang or 'ru'
    books_text = get_books_list_text(books[start_idx:end_idx], start_idx, lang)
    keyboard = []
    buttons = []
    for i in range(start_idx, end_idx):
        buttons.append(InlineKeyboardButton(
            f"📚 {i+1}",
            callback_data=f"book_{i}"
        ))
        if len(buttons) >= 5:
            keyboard.append(buttons)
            buttons = []
    if buttons:
        keyboard.append(buttons)
    pagination_buttons = []
    if current_page > 0:
        pagination_buttons.append(
            InlineKeyboardButton(get_text("btn_back", lang), callback_data="prev_page")
        )
    if current_page < total_pages - 1:
        pagination_buttons.append(
            InlineKeyboardButton(get_text("btn_next", lang), callback_data="next_page")
        )
    if pagination_buttons:
        keyboard.append(pagination_buttons)
    keyboard.append([InlineKeyboardButton(get_text("btn_cancel", lang), callback_data="cancel")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    message_text = get_text(
        "search_found", lang,
        total=total_books,
        page=current_page + 1,
        pages=total_pages,
        books=books_text
    )
    return reply_markup, message_text

async def perform_search(update: Update, context: CallbackContext) -> int:
    """Выполнение поиска и вывод результатов с пагинацией"""
    logger.debug("perform_search() start")
    message = update.message if update.message else update.edited_message
    # Показываем статус "печатает"
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING
    )
    query = context.user_data['search_query']
    search_type = context.user_data['search_type']
    current_page = context.user_data.get('current_page', 0)
    context.user_data['current_page'] = current_page
    logger.info("query=%s search_type=%s current_page=%s", query, search_type, current_page)
    lang = auth.get_language(update.effective_user.id)
    if 'search_results' not in context.user_data:
        books = search_books(query, search_type)
        if not books:
            await message.reply_text(get_text("nothing_found", lang))
            return reset_search(context)
        context.user_data['search_results'] = books
    else:
        books = context.user_data['search_results']
    reply_markup, message_text = get_books_search_message_with_buttons(books, current_page, lang)
    if 'search_message_id' in context.user_data:
        try:
            await context.bot.edit_message_text(
                chat_id=update.effective_chat.id,
                message_id=context.user_data['search_message_id'],
                text=message_text,
                parse_mode="HTML",
                reply_markup=reply_markup
            )
        except TelegramError as e:
            logger.error("Ошибка при редактировании сообщения: %s", str(e))
            msg = await message.reply_text(
                message_text,
                parse_mode="HTML",
                reply_markup=reply_markup
            )
            context.user_data['search_message_id'] = msg.message_id
    else:
        msg = await message.reply_text(
            message_text,
            parse_mode="HTML",
            reply_markup=reply_markup
        )
        context.user_data['search_message_id'] = msg.message_id

    return BOOK_SELECT
