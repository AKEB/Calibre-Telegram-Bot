"""Функции для Статистики"""
import os
import sqlite3
from config import logger, BOOKS_IMPORT_DIR, CALIBRE_DB
from utils import count_files_by_pattern
from texts import get_text
from auth import Auth

auth = Auth()

def get_stats() -> dict:
    """Возвращает статистику библиотеки"""
    logger.debug("get_stats() start")
    stat = dict(
        books=0,
        authors=0,
        series=0,
        categories=0,
        languages=0,
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

        cursor.execute("SELECT COUNT(*) FROM languages")
        language_count = cursor.fetchone()
        if language_count:
            stat['languages'] = int(language_count[0])

        cursor.execute("SELECT format, COUNT(*) FROM data GROUP BY format")
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

def get_stats_message(lang=None) -> str|None:
    """Возвращает статистику библиотеки"""
    logger.debug("get_stats_message() start")
    message = ''
    try:
        stats = get_stats()
        if not stats:
            logger.error("Не удалось получить статистику из базы данных")
            return None
        lang = lang or 'ru'
        message += get_text("stats_header", lang)
        message += get_text(
            "stats_books", lang, books=f"{stats.get('books', 0):,}".replace(',', ' ')
        )
        message += get_text(
            "stats_authors", lang, authors=f"{stats.get('authors', 0):,}".replace(',', ' ')
        )
        message += get_text(
            "stats_categories", lang, categories=f"{stats.get('categories', 0):,}".replace(',', ' ')
        )
        message += get_text(
            "stats_series", lang, series=f"{stats.get('series', 0):,}".replace(',', ' ')
        )
        message += get_text(
            "stats_languages", lang, languages=f"{stats.get('languages', 0):,}".replace(',', ' ')
        )
        message += get_text(
            "stats_formats", lang, formats=f"{len(stats.get('formats', {})):,}".replace(',', ' ')
        )
        if stats.get('formats'):
            for fmt, count in stats['formats'].items():
                message += get_text(
                    "stats_format_row", lang,
                    fmt=fmt, count=f"{count:,}".replace(',', ' ')
                )
        if BOOKS_IMPORT_DIR:
            message += get_text("stats_import_header", lang)
            stats_queue = count_files_by_pattern(
                os.path.join(BOOKS_IMPORT_DIR, "import/"),
                '*.*'
            )
            message += get_text(
                "stats_import_queue", lang, count=f"{stats_queue:,}".replace(',', ' ')
            )
            stats_error = count_files_by_pattern(
                os.path.join(BOOKS_IMPORT_DIR, "import_error/"),
                '*.*'
            )
            message += get_text(
                "stats_import_error", lang, count=f"{stats_error:,}".replace(',', ' ')
            )
        return message
    except sqlite3.Error as e:
        logger.error("Ошибка базы данных при получении статистики: %s", str(e))
        return None
    except (OSError, IOError) as e:
        logger.error("Ошибка файловой системы при получении статистики: %s", str(e))
        return None
