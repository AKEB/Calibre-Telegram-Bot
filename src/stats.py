"""Функции для Статистики"""
import os
import sqlite3
from config import logger, BOOKS_IMPORT_DIR, CALIBRE_DB
from utils import count_files_by_pattern

def get_stats() -> dict:
    """Возвращает статистику библиотеки"""
    logger.debug("get_stats() start")
    stat = dict(
        books=0,
        authors=0,
        series=0,
        categories=0,
        languages=dict(),
        formats=dict()
    )
    try:
        conn = sqlite3.connect(f'file:{CALIBRE_DB}?mode=ro', uri=True)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM books")
        books_count = cursor.fetchone()
        if books_count:
            stat['books'] = int(books_count[0])

        cursor.execute("SELECT COUNT(*) FROM authors")
        authors_count = cursor.fetchone()
        if authors_count:
            stat['authors'] = int(authors_count[0])

        cursor.execute("SELECT COUNT(*) FROM series")
        series_count = cursor.fetchone()
        if series_count:
            stat['series'] = int(series_count[0])

        cursor.execute("SELECT COUNT(*) FROM tags")
        tags_count = cursor.fetchone()
        if tags_count:
            stat['categories'] = int(tags_count[0])

        cursor.execute("SELECT lang_code,COUNT(*) FROM languages GROUP BY lang_code")
        languages_count = cursor.fetchall()
        if languages_count:
            stat['languages'] = {lang[0]: int(lang[1]) for lang in languages_count}

        cursor.execute("SELECT format,COUNT(*) FROM data GROUP BY format")
        formats_count = cursor.fetchall()
        if formats_count:
            stat['formats'] = {format[0]: int(format[1]) for format in formats_count}
    except sqlite3.Error as e:
        logger.error("Ошибка базы данных при получении статистики: %s", str(e))
        return stat
    except (OSError, IOError) as e:
        logger.error("Ошибка файловой системы при получении статистики: %s", str(e))
        return stat
    finally:
        if 'conn' in locals():
            conn.close()
    logger.info("Статистика библиотеки: %s", stat)
    return stat

def get_stats_message() -> str|None:
    """Возвращает статистику библиотеки"""
    logger.debug("get_stats_message() start")
    message = ''
    try:
        stats = get_stats()
        if not stats:
            logger.error("Не удалось получить статистику из базы данных")
            return None
        message += (
            "📊 Статистика библиотеки:\n\n"
            f"📚 Книг: {stats.get('books', 0):,}\n"
            f"✍️ Авторов: {stats.get('authors', 0):,}\n"
            f"🏷️ Категорий: {stats.get('categories', 0):,}\n"
            f"📖 Серий: {stats.get('series', 0):,}\n"
        ).replace(',', ' ')
        # Подробная статистика по языкам
        message += f"\n🌐 Языков: {len(stats.get('languages', {})):,}\n"
        if stats.get('languages'):
            for lang, count in stats['languages'].items():
                message += f"\t\t\t  - {lang}: {count:,}\n".replace(',', ' ')

        message += f"\n📁 Форматов: {len(stats.get('formats', {})):,}\n"
        # Подробная статистика по форматам
        if stats.get('formats'):
            for fmt, count in stats['formats'].items():
                message += f"\t\t\t  - {fmt}: {count:,}\n".replace(',', ' ')

        if BOOKS_IMPORT_DIR:
            message += "\n📥 Импорт книг:\n"

            stats = count_files_by_pattern(
                os.path.join(BOOKS_IMPORT_DIR, "import/"),
                '*.*'
            )
            message += f"\t\t\t  - в очереди: {stats:,}\n".replace(',', ' ')

            stats_error = count_files_by_pattern(
                os.path.join(BOOKS_IMPORT_DIR, "import_error/"),
                '*.*'
            )
            message += f"\t\t\t  - ошибок: {stats_error:,}\n".replace(',', ' ')

        return message
    except sqlite3.Error as e:
        logger.error("Ошибка базы данных при получении статистики: %s", str(e))
        return None
    except (OSError, IOError) as e:
        logger.error("Ошибка файловой системы при получении статистики: %s", str(e))
        return None
