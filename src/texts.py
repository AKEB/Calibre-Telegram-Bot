"""
Тексты для мультиязычности бота
Для добавления нового языка — добавьте ключ с нужным языковым кодом
"""
BOT_TEXTS = {
    "start": {
        "ru": (
            "📚 Добро пожаловать в библиотеку Calibre!\n\n"
            "Вы можете искать книги по:\n"
            "- Названию (/title <название>)\n"
            "- Автору (/author <автор>)\n"
            "- Серии (/series <серия>)\n"
            "- Любому ключевому слову (/search <запрос>) или просто <запрос>\n\n"
            "Также доступны команды для:\n"
            "- /random - покажет {RANDOM_BOOKS_COUNT} случайных книг из библиотеки\n"
            "- Поиску книги по ID (/id <идентификатор>)"
            " - идентификатор можно найти в сообщении о книге\n"
            "- Загрузить книгу на сервер (/upload) - отправьте файл книги или укажите URL\n"
            "- Статистика библиотеки (/stats) - покажет количество книг, авторов и т.д.\n\n"
            "Команды для администраторов:\n"
            "- Добавить пользователя в авторизованные (/add <user_id>)"
            " - для управления доступом\n\n"
            "Для получения справки по командам используйте команду /help\n\n"
            "📖 Библиотека содержит множество книг в разных форматах (EPUB, FB2, MOBI и т.д.).\n"
            "Вы можете скачивать книги в удобном для вас формате.\n\n"
            "Если у вас есть вопросы или предложения, обратитесь к администратору.\n\n"
            "Для начала поиска книг используйте команду /search или просто введите запрос.\n\n"
            "Пример: /search Гарри Поттер\n\n"
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
        ),
        "en": (
            "📚 Welcome to the Calibre Library!\n\n"
            "You can search for books by:\n"
            "- Title (/title <title>)\n"
            "- Author (/author <author>)\n"
            "- Series (/series <series>)\n"
            "- Any keyword (/search <query>) or just <query>\n\n"
            "Other available commands:\n"
            "- /random - shows {RANDOM_BOOKS_COUNT} random books from the library\n"
            "- Search by book ID (/id <id>) - the ID can be found in the book message\n"
            "- Upload a book to the server (/upload) - send a book file or specify a URL\n"
            "- Library statistics (/stats) - shows the number of books, authors, etc.\n\n"
            "Admin commands:\n"
            "- Add a user to authorized (/add <user_id>) - for access management\n\n"
            "For help, use the /help command\n\n"
            "📖 The library contains many books in different formats (EPUB, FB2, MOBI, etc.).\n"
            "You can download books in your preferred format.\n\n"
            "If you have questions or suggestions, contact the administrator.\n\n"
            "To start searching for books, use the /search command or just enter a query.\n\n"
            "Example: /search Harry Potter\n\n"
            "You can also just enter a text query without a command, and the bot "
            "will try to find books by your query.\n\n"
            "Advanced search examples:\n"
            "- title:Harry Potter - search by title\n"
            "- title:=Harry Potter - exact title search\n"
            "- author:J.K. Rowling - search by author\n"
            "- author:=J.K. Rowling - exact author search\n"
            "- series:Harry Potter - search by series\n"
            "- series:=Harry Potter - exact series search\n"
            "- tags:fantasy - search by tags\n"
            "- tags:=fantasy - exact tag search\n"
            "- publisher:Bloomsbury - search by publisher\n"
            "- publisher:=Bloomsbury - exact publisher search\n"
            "- languages:english - search by language\n"
            "- languages:=english - exact language search\n"
            "- formats:fb2 - search by format\n"
            "- formats:=fb2 - exact format search\n\n"
            "You can also combine commands:\n"
            "- title:Harry Potter and author:J.K. Rowling - search by title and author\n"
        )
    }
}

BOT_TEXTS.update({
    "access_denied": {
        "ru": (
            "⛔ Доступ запрещен\n"
            "      Обратитесь к администратору для получения доступа\n"
            "      Ваш ID={user_id}"
        ),
        "en": (
            "⛔ Access denied\n"
            "      Please contact the administrator for access\n"
            "      Your ID={user_id}"
        )
    },
    "admin_only": {
        "ru": "⛔ У вас нет прав для выполнения этой команды.",
        "en": "⛔ You do not have permission to execute this command."
    },
    "cancelled": {
        "ru": "Отменено.",
        "en": "Cancelled."
    },
    "empty_value": {
        "ru": "Пожалуйста, введите непустое значение",
        "en": "Please enter a non-empty value"
    },
    "add_usage": {
        "ru": "Использование: /add <user_id>",
        "en": "Usage: /add <user_id>"
    },
    "add_id_number": {
        "ru": "ID пользователя должен быть числом",
        "en": "User ID must be a number"
    },
    "already_authorized": {
        "ru": "Пользователь {user_id} уже есть в списке авторизованных",
        "en": "User {user_id} is already authorized"
    },
    "add_success": {
        "ru": "✅ Пользователь {user_id} успешно добавлен",
        "en": "✅ User {user_id} successfully added"
    },
    "add_error": {
        "ru": "Произошла ошибка при добавлении пользователя",
        "en": "An error occurred while adding the user"
    },
    "operation_cancelled": {
        "ru": "Операция отменена.",
        "en": "Operation cancelled."
    },
    "error_occurred": {
        "ru": "😞 Произошла ошибка. Попробуйте еще раз.",
        "en": "😞 An error occurred. Please try again."
    },
    "stats_error": {
        "ru": "Не удалось получить статистику. Попробуйте позже.",
        "en": "Failed to get statistics. Please try again later."
    },
    "language_select": {
        "ru": "Выберите язык / Select language:",
        "en": "Выберите язык / Select language:"
    },
    "lang_set_ru": {
        "ru": "Язык успешно изменён на Русский 🇷🇺",
        "en": "Language successfully set to Russian 🇷🇺"
    },
    "lang_set_en": {
        "ru": "Language successfully set to English 🇬🇧",
        "en": "Language successfully set to English 🇬🇧"
    },
    "lang_set_unknown": {
        "ru": "Неизвестный выбор / Unknown selection",
        "en": "Unknown selection / Неизвестный выбор"
    },
    "prompt_search": {
        "ru": "🔍 Введите поисковый запрос (название, автор или ключевые слова):",
        "en": "🔍 Enter a search query (title, author, or keywords):"
    },
    "prompt_series": {
        "ru": "📚 Введите название серии для поиска:",
        "en": "📚 Enter the series name to search:"
    },
    "prompt_title": {
        "ru": "📖 Введите название книги для поиска:",
        "en": "📖 Enter the book title to search:"
    },
    "prompt_author": {
        "ru": "✍️ Введите имя автора для поиска:",
        "en": "✍️ Enter the author's name to search:"
    },
    "prompt_id": {
        "ru": "#️⃣ Введите ID книги для поиска:",
        "en": "#️⃣ Enter the book ID to search:"
    },
    "prompt_upload": {
        "ru": (
            "📤 Отправьте файл книги (EPUB, FB2, MOBI и т.д.) "
            "или укажите URL книги после команды /upload"
        ),
        "en": (
            "📤 Send a book file (EPUB, FB2, MOBI, etc.) "
            "or specify the book URL after the /upload command"
        )
    },
    "prepare_format": {
        "ru": "⏳ Подготавливаю книгу в формате {fmt}...",
        "en": "⏳ Preparing the book in {fmt} format..."
    },
    "file_too_large": {
        "ru": "⚠️ Файл слишком большой. Максимальный размер: {max_mb}MB",
        "en": "⚠️ File is too large. Maximum size: {max_mb}MB"
    },
    "unsupported_format": {
        "ru": "⚠️ Неподдерживаемый формат файла. Допустимые форматы: {formats}",
        "en": "⚠️ Unsupported file format. Allowed formats: {formats}"
    },
    "telegram_error": {
        "ru": "⚠️ Ошибка Telegram: {error}",
        "en": "⚠️ Telegram error: {error}"
    },
    "fs_error": {
        "ru": "⚠️ Ошибка файловой системы: {error}",
        "en": "⚠️ Filesystem error: {error}"
    },
    "url_error": {
        "ru": "⚠️ Ошибка при загрузке по URL: {error}",
        "en": "⚠️ Error downloading by URL: {error}"
    },
    "add_success_calibre": {
        "ru": "✅ Книга успешно добавлена в библиотеку! ID: {book_id}",
        "en": "✅ Book successfully added to the library! ID: {book_id}"
    },
    "add_success_calibre_noid": {
        "ru": "✅ Книга успешно добавлена в библиотеку!\n{stdout}",
        "en": "✅ Book successfully added to the library!\n{stdout}"
    },
    "add_error_calibre": {
        "ru": "⚠️ Ошибка при добавлении книги:\n{error}",
        "en": "⚠️ Error adding book:\n{error}"
    },
    "timeout_calibre": {
        "ru": "⚠️ Превышено время ожидания добавления книги",
        "en": "⚠️ Book adding timeout exceeded"
    },
    "nothing_found": {
        "ru": "😞 Ничего не найдено. Попробуйте другой запрос.",
        "en": "😞 Nothing found. Try another query."
    },
})

BOT_TEXTS.update({
    "book_card": {
        "ru": (
            "📚 Выбрана: <b>{title}</b>\n"
            "✍️ Автор: {author}\n"
            "📖 Серия: {series} [{series_index}]\n"
            "{publisher_block}"
            "Идентификатор: {id}\n"
            "Жанр: {tags}\n"
            "Описание: <blockquote>{desc}</blockquote>\n\n"
            "{download_block}"
        ),
        "en": (
            "📚 Selected: <b>{title}</b>\n"
            "✍️ Author: {author}\n"
            "📖 Series: {series} [{series_index}]\n"
            "{publisher_block}"
            "ID: {id}\n"
            "Genre: {tags}\n"
            "Description: <blockquote>{desc}</blockquote>\n\n"
            "{download_block}"
        )
    },
    "book_download_block": {
        "ru": (
            "Выберите формат для скачивания:\n"
            "✅ - доступен сразу\n"
            "🔄 - будет сконвертирован из доступного формата"
        ),
        "en": (
            "Choose a format to download:\n"
            "✅ - available immediately\n"
            "🔄 - will be converted from available format"
        )
    },
    "publisher": {
        "ru": "Издатель: {publisher}",
        "en": "Publisher: {publisher}"
    },
    "btn_back": {
        "ru": "⬅️ Назад",
        "en": "⬅️ Back"
    },
    "btn_cancel": {
        "ru": "❌ Отмена",
        "en": "❌ Cancel"
    },
})

BOT_TEXTS.update({
    "prepare_failed": {
        "ru": "😞 Не удалось подготовить книгу. Попробуйте другой формат.",
        "en": "😞 Failed to prepare the book. Try another format."
    },
    "send_success": {
        "ru": "✅ Книга отправлена в формате {fmt}!",
        "en": "✅ Book sent in {fmt} format!"
    },
    "send_error": {
        "ru": "😞 Произошла ошибка при отправке файла.",
        "en": "😞 An error occurred while sending the file."
    },
})

BOT_TEXTS.update({
    "btn_next": {
        "ru": "Вперед ➡️",
        "en": "Next ➡️"
    },
    "search_found": {
        "ru": (
            "🔍 Найдено {total} книг. Страница {page}/{pages}\n\n"
            "{books}\nВыберите книгу или перейдите на другую страницу:"
        ),
        "en": (
            "🔍 Found {total} books. Page {page}/{pages}\n\n"
            "{books}\nSelect a book or go to another page:"
        )
    },
    "search_id": {
        "ru": "ID: {id}",
        "en": "ID: {id}"
    },
    "search_publisher": {
        "ru": "{publisher}",
        "en": "{publisher}"
    },
    "search_size": {
        "ru": "({size})",
        "en": "({size})"
    },
    "search_series": {
        "ru": "📖 {series} [{series_index}]",
        "en": "📖 {series} [{series_index}]"
    },
    "search_genre": {
        "ru": "Жанр: {tags}",
        "en": "Genre: {tags}"
    },
})

BOT_TEXTS.update({
    "stats_header": {
        "ru": "📊 Статистика библиотеки:\n\n",
        "en": "📊 Library statistics:\n\n"
    },
    "stats_books": {
        "ru": "📚 Книг: {books}\n",
        "en": "📚 Books: {books}\n"
    },
    "stats_authors": {
        "ru": "✍️ Авторов: {authors}\n",
        "en": "✍️ Authors: {authors}\n"
    },
    "stats_categories": {
        "ru": "🏷️ Категорий: {categories}\n",
        "en": "🏷️ Categories: {categories}\n"
    },
    "stats_series": {
        "ru": "📖 Серий: {series}\n",
        "en": "📖 Series: {series}\n"
    },
    "stats_languages": {
        "ru": "🌐 Языков: {languages}\n",
        "en": "🌐 Languages: {languages}\n"
    },
    "stats_formats": {
        "ru": "📁 Форматов: {formats}\n",
        "en": "📁 Formats: {formats}\n"
    },
    "stats_format_row": {
        "ru": "\t\t\t  - {fmt}: {count}\n",
        "en": "\t\t\t  - {fmt}: {count}\n"
    },
    "stats_import_header": {
        "ru": "\n📥 Импорт книг:\n",
        "en": "\n📥 Book import:\n"
    },
    "stats_import_queue": {
        "ru": "\t\t\t  - в очереди: {count}\n",
        "en": "\t\t\t  - in queue: {count}\n"
    },
    "stats_import_error": {
        "ru": "\t\t\t  - ошибок: {count}\n",
        "en": "\t\t\t  - errors: {count}\n"
    },
})

def get_text(section, lang, **kwargs):
    """Получить текст для секции и языка, с подстановкой переменных"""
    txt = BOT_TEXTS.get(section, {}).get(lang)
    if not txt:
        txt = BOT_TEXTS.get(section, {}).get('ru', '')
    return txt.format(**kwargs) if txt else ''
