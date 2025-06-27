"""Обработчики команд и сообщений"""

import time
from functools import wraps
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, LinkPreviewOptions
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext,
    CallbackQueryHandler,
    ConversationHandler
)
from auth import Auth
from config import logger, RANDOM_BOOKS_COUNT, CALIBRE_WEB_URL
from config import (SEARCH, BOOK_SELECT, FORMAT_SELECT, REQUEST_SEARCH, REQUEST_TITLE,
                    REQUEST_AUTHOR, REQUEST_SERIES, REQUEST_ID, REQUEST_UPLOAD
                    )
from upload_file import handle_url_upload, handle_document_upload
from stats import get_stats_message
from reset import reset_last_command, reset_search
from download import format_selected
from search import perform_search
from book import book_selected

auth = Auth()


def permission_required(is_admin: bool = False):
    """Decorator for checking permissions"""
    def outer_wrapper(fn):
        @wraps(fn)
        async def wrapper(*args, **kwargs):
            update: Update = args[0]
            context: CallbackContext = args[1]

            await context.bot.send_chat_action(
                chat_id=update.effective_chat.id,
                action=ChatAction.TYPING
            )

            if not is_admin and not auth.is_authorized(update.effective_user.id):
                await (update.message if update.message else update.edited_message).reply_text(
                    "⛔ Доступ запрещен\n" +
                    "      Обратитесь к администратору для получения доступа\n" +
                    f"      Ваш ID={update.effective_user.id}"
                )
                return reset_last_command(context)

            # Только для администратора
            if is_admin and not auth.is_admin(update.effective_user.id):
                await (update.message if update.message else update.edited_message
                       ).reply_text("⛔ У вас нет прав для выполнения этой команды.")
                return reset_last_command(context)

            return await fn(*args, **kwargs)
        return wrapper
    return outer_wrapper

# ==========================================================================

# Handlers


@permission_required()
async def book_selected_handler(update: Update, context: CallbackContext) -> int:
    """Обработка выбора книги"""
    logger.debug("book_selected_handler() start")
    query = update.callback_query
    await query.answer()

    if query.data in ['prev_page', 'next_page'] or query.data.startswith('page_'):
        return await pagination_handler(update, context)

    if query.data.startswith('cancel'):
        await query.edit_message_text("Отменено.")
        return reset_search(context)

    book_index = int(query.data.split('_')[1])
    book = context.user_data['search_results'][book_index]
    context.user_data['selected_book'] = book

    link_preview_options = None
    # Если задан URL для предпросмотра обложки книги
    # Используем CALIBRE_WEB_URL для получения обложки книги
    if CALIBRE_WEB_URL:
        cover_url = str(CALIBRE_WEB_URL).format(str(book['id']), str(time.time()))
        logger.warning(
            "book_selected_handler() cover_url: %s", cover_url)
        link_preview_options = LinkPreviewOptions(
            is_disabled=False,
            url=cover_url
        )

    reply_markup, text = book_selected(book)

    await (
        update.message if update.message else update.edited_message
          ).reply_text(
        text,
        parse_mode="HTML",
        reply_markup=reply_markup,
        link_preview_options=link_preview_options
    )

    return FORMAT_SELECT


@permission_required()
async def perform_search_handler(update: Update, context: CallbackContext) -> int:
    """Выполнение поиска и вывод результатов с пагинацией"""
    logger.debug("perform_search_handler() start")
    return await perform_search(update, context)


@permission_required()
async def format_selected_handler(update: Update, context: CallbackContext) -> int:
    """Обработка выбора формата"""
    logger.debug("format_selected_handler() start")
    query = update.callback_query
    await query.answer()

    if query.data == 'cancel':
        await query.edit_message_text("Отменено.")
        return reset_search(context)

    if query.data == 'back':
        return await perform_search(update, context)

    selected_format = query.data.split('_')[1]
    book = context.user_data['selected_book']

    await query.edit_message_text(f"⏳ Подготавливаю книгу в формате {selected_format.upper()}...")

    # Показываем статус "загружает документ"
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.UPLOAD_DOCUMENT
    )

    message = await format_selected(book, selected_format, context, update.effective_chat.id)

    await query.edit_message_text(message)
    return reset_search(context)


@permission_required()
async def handle_parameter_response_handler(update: Update, context: CallbackContext) -> int:
    """Обрабатывает ответ пользователя с запрошенным параметром"""
    logger.debug("handle_parameter_response_handler() start")

    message = update.message if update.message else update.edited_message
    if message and message.text:
        logger.warning(
            "handle_parameter_response_handler() called with message text: %s", message.text)

    param_value = message.text.strip() if message and message.text else ''
    if not param_value:
        await message.reply_text("Пожалуйста, введите непустое значение")
        return globals()[f"REQUEST_{context.user_data['current_command'].upper()}"]

    reset_last_command(context)

    context.user_data['search_query'] = param_value
    context.user_data['awaiting_parameter'] = False

    # Определяем, какую команду продолжаем выполнять
    command = context.user_data['current_command']
    if command == 'search':
        context.user_data['search_type'] = 'all'
        return await perform_search(update, context)
    elif command == 'title':
        context.user_data['search_type'] = 'title'
        return await perform_search(update, context)
    elif command == 'author':
        context.user_data['search_type'] = 'author'
        return await perform_search(update, context)
    elif command == 'series':
        context.user_data['search_type'] = 'series'
        return await perform_search(update, context)
    elif command == 'random':
        context.user_data['search_type'] = 'random'
        return await perform_search(update, context)
    elif command == 'id':
        context.user_data['search_type'] = 'id'
        return await perform_search(update, context)
    elif command == 'upload':
        return await handle_url_upload(update, context, param_value)
    return ConversationHandler.END


@permission_required()
async def pagination_handler(update: Update, context: CallbackContext) -> int:
    """Обработка переключения страниц"""
    logger.debug("pagination_handler() start")
    query = update.callback_query
    await query.answer()

    action = query.data

    if action == 'prev_page':
        context.user_data['current_page'] -= 1
    elif action == 'next_page':
        context.user_data['current_page'] += 1

    return await perform_search(update, context)


@permission_required()
async def search_handler(update: Update, context: CallbackContext) -> int:
    """Обработка команды поиска"""
    logger.debug("search_handler() start")
    reset_search(context)

    message = update.message if update.message else update.edited_message
    if message and message.text:
        logger.warning(
            "search_handler() called with message text: %s", message.text)

    context.user_data['current_command'] = 'search'
    if (
        not context.args and
        (
            not message or
            not message.text or
            not message.text.strip() or
            message.text.strip() == '/search'
        )
    ):
        return await request_parameter(
            update,
            context,
            "🔍 Введите поисковый запрос (название, автор или ключевые слова):"
        )

    query = (' '.join(context.args) if context.args
             else message.text.replace('/search', '').strip()
             )
    context.user_data['search_type'] = 'all'
    context.user_data['search_query'] = query
    return await perform_search(update, context)


@permission_required()
async def series_handler(update: Update, context: CallbackContext) -> int:
    """Обработка команды поиска по серии"""
    logger.debug("series_handler() start")
    reset_last_command(context)
    context.user_data['current_command'] = 'series'

    if not context.args:
        return await request_parameter(
            update,
            context,
            "📚 Введите название серии для поиска:"
        )

    context.user_data['search_type'] = 'series'
    context.user_data['search_query'] = ' '.join(context.args)
    return await perform_search(update, context)


@permission_required()
async def title_handler(update: Update, context: CallbackContext) -> int:
    """Обработка команды поиска по названию"""
    logger.debug("title_handler() start")

    reset_last_command(context)

    context.user_data['current_command'] = 'title'

    if not context.args:
        return await request_parameter(
            update,
            context,
            "📖 Введите название книги для поиска:"
        )

    context.user_data['search_type'] = 'title'
    context.user_data['search_query'] = ' '.join(context.args)
    return await perform_search(update, context)


@permission_required()
async def author_handler(update: Update, context: CallbackContext) -> int:
    """Обработка команды поиска по автору"""
    logger.debug("author_handler() start")

    reset_last_command(context)
    context.user_data['current_command'] = 'author'

    if not context.args:
        return await request_parameter(
            update,
            context,
            "✍️ Введите имя автора для поиска:"
        )

    context.user_data['search_type'] = 'author'
    context.user_data['search_query'] = ' '.join(context.args)
    return await perform_search(update, context)


@permission_required()
async def random_handler(update: Update, context: CallbackContext) -> int:
    """Обработка команды поиска по серии"""
    logger.debug("random_handler() start")

    reset_last_command(context)
    context.user_data['current_command'] = 'random'

    context.user_data['search_type'] = 'random'
    context.user_data['search_query'] = ' '.join(context.args)
    return await perform_search(update, context)


@permission_required()
async def id_handler(update: Update, context: CallbackContext) -> int:
    """Обработка команды поиска по ID"""
    logger.debug("id_handler() start")

    reset_last_command(context)
    context.user_data['current_command'] = 'id'

    if not context.args:
        return await request_parameter(
            update,
            context,
            "#️⃣ Введите ID книги для поиска:"
        )

    context.user_data['search_type'] = 'id'
    context.user_data['search_query'] = ' '.join(context.args)
    return await perform_search(update, context)

# pylint: disable=W0613


@permission_required()
async def stats_handler(update: Update, context: CallbackContext) -> None:
    """Обработка команды /stats - возвращает статистику библиотеки"""
    logger.debug("stats_handler() start")

    message = get_stats_message()
    if not message:
        await (update.message if update.message else update.edited_message
               ).reply_text("Не удалось получить статистику. Попробуйте позже.")
    else:
        await (update.message if update.message else update.edited_message).reply_text(message)


# pylint: disable=C0301
@permission_required()
async def start_handler(update: Update, context: CallbackContext) -> int:
    """Обработка команды /start"""
    logger.debug("start_handler() start")
    reset_last_command(context)

    await (update.message if update.message else update.edited_message).reply_text(
        "📚 Добро пожаловать в библиотеку Calibre!\n\n"

        "Вы можете искать книги по:\n"
        "- Названию (/title <название>)\n"
        "- Автору (/author <автор>)\n"
        "- Серии (/series <серия>)\n"
        "- Любому ключевому слову (/search <запрос>) или просто <запрос>\n\n"

        "Также доступны команды для:\n"
        f"- /random - покажет {RANDOM_BOOKS_COUNT} случайных книг из библиотеки\n"
        "- Поиску книги по ID (/id <идентификатор>) - идентификатор можно найти в сообщении о книге\n"
        "- Загрузить книгу на сервер (/upload) - отправьте файл книги или укажите URL\n"
        "- Статистика библиотеки (/stats) - покажет количество книг, авторов и т.д.\n\n"

        "Команды для администраторов:\n"
        "- Добавить пользователя в авторизованные (/add <user_id>) - для управления доступом\n\n"

        "Для получения справки по командам используйте команду /help\n\n"

        "📖 Библиотека содержит множество книг в разных форматах (EPUB, FB2, MOBI и т.д.).\n"
        "Вы можете скачивать книги в удобном для вас формате.\n\n"
        "Если у вас есть вопросы или предложения, обратитесь к администратору.\n\n"
        "Для начала поиска книг используйте команду /search или просто введите запрос.\n\n"

        "Пример: /search Гарри Поттер\n"

        "Также вы можете просто ввести текстовый запрос без команды, и бот "
        "попытается найти книги по этому запросу.\n\n"
        "Доступны сложные поиски например:\n"
        "- title:Гарри Поттер - поиск по названию\n"
        "- title:=Гарри Поттер - поиск по точному названию\n"
        "- author:Джоан Роулинг - поиск по автору\n"
        "- author:=Джоан Роулинг - поиск по точному автору\n"
        "- series:Гарри Поттер - поиск по серии\n"
        "- series:=Гарри Поттер - поиск по точной серии\n"
        "- tags:фэнтези - поиск по тегам\n"
        "- tags:=фэнтези - поиск по точным тегам\n"
        "- publisher:Bloomsbury - поиск по издателю\n"
        "- publisher:=Bloomsbury - поиск по точному издателю\n"
        "- languages:русский - поиск по языкам\n"
        "- languages:=русский - поиск по точному языку\n"
        "- formats:fb2 - поиск по формату\n"
        "- formats:=fb2 - поиск по точному формату\n\n"

        "А также доступны различные сочетания команд:\n"
        "- title:Гарри Поттер and author:Джоан Роулинг - поиск по названию и автору\n"


    )
    return reset_search(context)


@permission_required()
async def upload_book_handler(update: Update, context: CallbackContext) -> int:
    """Обработка команды загрузки книги"""
    logger.debug("upload_book_handler() start")

    reset_last_command(context)
    context.user_data['current_command'] = 'upload'

    # Если команда вызвана без параметров (просто /upload)
    if not update.message.document and not context.args:
        return await request_parameter(
            update,
            context,
            "📤 Отправьте файл книги (EPUB, FB2, MOBI и т.д.) "
            "или укажите URL книги после команды /upload"
        )

    # Остальная логика обработки загрузки без изменений...
    if context.args:
        return await handle_url_upload(update, context, ' '.join(context.args))
    else:
        return await handle_document_upload(update, context)


@permission_required(True)
async def add_user_handler(update: Update, context: CallbackContext) -> None:
    """Обработка команды /add - добавление пользователя в авторизованные"""
    logger.debug("add_user_handler() start")

    if not context.args:
        await (update.message if update.message else update.edited_message
               ).reply_text("Использование: /add <user_id>")
        return reset_last_command(context)

    new_user_id = context.args[0]
    if not new_user_id.isdigit():
        await (update.message if update.message else update.edited_message
               ).reply_text("ID пользователя должен быть числом")
        return reset_last_command(context)

    # Проверяем, есть ли уже такой пользователь
    if auth.is_authorized(new_user_id):
        await (update.message if update.message else update.edited_message).reply_text(
            f"Пользователь {new_user_id} уже есть в списке авторизованных"
        )
        return reset_last_command(context)

    if auth.add_authorized_user(new_user_id):
        await (update.message if update.message else update.edited_message
               ).reply_text(f"✅ Пользователь {new_user_id} успешно добавлен")
    else:
        await (update.message if update.message else update.edited_message
               ).reply_text("Произошла ошибка при добавлении пользователя")

# ==========================================================================

# Other functions


async def cancel_handler(update: Update, context: CallbackContext) -> int:
    """Отмена операции"""
    logger.debug("cancel_handler() start")
    await (update.message if update.message else update.edited_message
           ).reply_text('Операция отменена.')
    return reset_search(context)


async def error_handler(update: Update, context: CallbackContext) -> None:
    """Обработка ошибок"""
    logger.debug("error_handler() start")
    logger.error("Исключение при обработке сообщения:", exc_info=context.error)
    if update and update.message:
        await (update.message if update.message else update.edited_message
               ).reply_text('😞 Произошла ошибка. Попробуйте еще раз.')


async def request_parameter(update: Update, context: CallbackContext, prompt: str) -> int:
    """Запрашивает у пользователя недостающий параметр"""
    logger.debug("request_parameter() start")
    keyboard = []
    keyboard.append([InlineKeyboardButton("❌ Отмена", callback_data="cancel")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await (update.message if update.message else update.edited_message
           ).reply_text(prompt, reply_markup=reply_markup)
    # Сохраняем информацию о том, какой параметр мы запрашиваем
    context.user_data['awaiting_parameter'] = True
    return globals()[f"REQUEST_{context.user_data['current_command'].upper()}"]

# ==========================================================================

# Setup


def conversation_handler() -> ConversationHandler:
    """conversation_handler"""
    param_handlers = [
        CallbackQueryHandler(format_selected_handler,
                             pattern='^(back|cancel)$'),
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_parameter_response_handler
        ),
    ]
    return ConversationHandler(
        entry_points=[
            CommandHandler('search', search_handler),
            CommandHandler('title', title_handler),
            CommandHandler('author', author_handler),
            CommandHandler('series', series_handler),
            CommandHandler('random', random_handler),
            CommandHandler('id', id_handler),
            CommandHandler('upload', upload_book_handler),
            MessageHandler(filters.TEXT & ~filters.COMMAND, search_handler)
        ],
        states={
            SEARCH: [
                MessageHandler(filters.TEXT & ~filters.COMMAND,
                               perform_search_handler)
            ],
            BOOK_SELECT: [
                CallbackQueryHandler(book_selected_handler, pattern='^book_'),
                CallbackQueryHandler(pagination_handler,
                                     pattern='^(prev_page|next_page)$'),
                CallbackQueryHandler(
                    book_selected_handler, pattern='^cancel$'),
                CommandHandler('search', search_handler),
                CommandHandler('title', title_handler),
                CommandHandler('author', author_handler),
                CommandHandler('series', series_handler),
                CommandHandler('random', random_handler),
                CommandHandler('id', id_handler),
                MessageHandler(filters.TEXT & ~filters.COMMAND, search_handler)
            ],
            FORMAT_SELECT: [
                CallbackQueryHandler(
                    format_selected_handler, pattern='^format_'),
                CallbackQueryHandler(
                    format_selected_handler, pattern='^(back|cancel)$'),
                CommandHandler('search', search_handler),
                CommandHandler('title', title_handler),
                CommandHandler('author', author_handler),
                CommandHandler('series', series_handler),
                CommandHandler('random', random_handler),
                CommandHandler('id', id_handler),
                MessageHandler(filters.TEXT & ~filters.COMMAND, search_handler)
            ],
            # Новые состояния для запроса параметров
            REQUEST_SEARCH: param_handlers,
            REQUEST_TITLE: param_handlers,
            REQUEST_AUTHOR: param_handlers,
            REQUEST_SERIES: param_handlers,
            REQUEST_ID: param_handlers,
            REQUEST_UPLOAD: param_handlers,
        },
        fallbacks=[CommandHandler('cancel', cancel_handler)],
        per_message=False,  # Явно указываем этот параметр
        per_chat=True,
        per_user=True
    )


def setup_handlers(application: Application):
    """Инициализация обработчиков"""
    logger.debug("setup_handlers() start")

    application.add_handler(MessageHandler(
        filters.Document.ALL & ~filters.COMMAND,
        upload_book_handler
    ))
    application.add_handler(CommandHandler("stats", stats_handler))
    application.add_handler(CommandHandler("add", add_user_handler))
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("help", start_handler))
    application.add_handler(CommandHandler("upload", upload_book_handler))
    application.add_handler(conversation_handler())
    application.add_error_handler(error_handler)
