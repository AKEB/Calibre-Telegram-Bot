"""Функции для работы с базой"""
import os
import subprocess
import json
import shlex
import sqlite3
from config import (logger, CALIBRE_DB, BOOKS_LIMIT_COUNT, RANDOM_BOOKS_COUNT,
                    CALIBRE_LIBRARY_URL, CALIBRE_LIBRARY_USER, CALIBRE_LIBRARY_PASS)

def check_db_permissions():
    """Проверка разрешений для чтения и записи в базу"""
    logger.debug("check_db_permissions() start")
    if not os.path.isfile(CALIBRE_DB):
        logger.error("База данных не найдена: %s", CALIBRE_DB)
        return False
    if not os.access(CALIBRE_DB, os.R_OK):
        logger.error("Нет прав на чтение базы данных: %s", CALIBRE_DB)
        return False
    logger.info("Права на базу данных корректны: %s", CALIBRE_DB)
    return True

def search_books_calibredb(query, search_type='all'):
    """Поиск книг в базе данных Calibre"""
    logger.debug("search_books_calibredb() start")

    base_cmd = [
        'calibredb', 'list',
        '--with-library', CALIBRE_LIBRARY_URL,
        '--username', CALIBRE_LIBRARY_USER,
        '--password', CALIBRE_LIBRARY_PASS,
        '--for-machine',
        '--fields',
        'authors,title,languages,tags,comments,series,series_index,size,formats,publisher',
    ]
    # Добавляем параметры поиска в зависимости от типа
    if search_type == 'title':
        base_cmd.extend(['--limit', f'{BOOKS_LIMIT_COUNT}'])
        base_cmd.extend(['--sort-by', 'title'])
        base_cmd.extend(['--search', f'title:{query}'])
    elif search_type == 'author':
        base_cmd.extend(['--limit', f'{BOOKS_LIMIT_COUNT}'])
        base_cmd.extend(['--sort-by', 'author_sort'])
        base_cmd.extend(['--search', f'authors:{query}'])
    elif search_type == 'series':
        base_cmd.extend(['--limit', f'{BOOKS_LIMIT_COUNT}'])
        base_cmd.extend(['--sort-by', 'series,series_index'])
        base_cmd.extend(['--search', f'series:{query}'])
    elif search_type == 'id':
        base_cmd.extend(['--limit', f'{BOOKS_LIMIT_COUNT}'])
        base_cmd.extend(['--sort-by', 'id'])
        base_cmd.extend(['--search', f'id:={query}'])
    elif search_type == 'random':
        logger.info("Поиск случайных книг")
        try:
            conn = sqlite3.connect(f'file:{CALIBRE_DB}?mode=ro', uri=True)
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM books ORDER BY RANDOM() LIMIT ?", (RANDOM_BOOKS_COUNT,))
            random_ids = cursor.fetchall()
            logger.info("Случайные id книг: %s", random_ids)
        except sqlite3.Error as e:
            logger.error("Ошибка базы данных при выполнении запроса: %s", str(e))
            return []
        except (OSError, IOError) as e:
            logger.error("Ошибка файловой системы при выполнении запроса: %s", str(e))
            return []
        finally:
            if 'conn' in locals():
                conn.close()
        if not random_ids:
            logger.error("Не удалось получить случайные id книг")
            return []
        random_ids = [rid[0] for rid in random_ids]
        if not random_ids:
            logger.error("Случайные id книг пусты")
            return []
        base_cmd.extend(['--limit', f'{RANDOM_BOOKS_COUNT}'])
        search = ' or '.join([f'id:={rid}' for rid in random_ids])
        base_cmd.extend(['--search', search])
        base_cmd.extend(['--sort-by', 'title'])
    else:
        base_cmd.extend(['--limit', f'{BOOKS_LIMIT_COUNT}'])
        base_cmd.extend(['--sort-by', 'title,author_sort,pubdate'])
        base_cmd.extend(['--search', query])

    try:
        logger.warning("QUERY_START: %s", {' '.join(
            shlex.quote(str(arg)) for arg in base_cmd)})

        # Выполняем команду и получаем вывод
        result = subprocess.run(
            base_cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        logger.warning('QUERY_END')

        # Парсим JSON вывод
        books_data = json.loads(result.stdout)

        # Преобразуем данные в нужный формат
        books = []
        for book in books_data:
            tags = book.get('tags', [])
            if isinstance(tags, list):
                tags_str = ', '.join(tags)
            else:
                tags_str = str(tags).replace(',', ', ')

            # if len(tags_str) > 50:
            #     tags_str = tags_str[:50] + '...'

            # Обработка авторов (может быть строкой с разделителями &)
            authors = book.get('authors', '')
            if isinstance(authors, str):
                authors_str = authors.replace('&', ', ')
            else:
                authors_str = ', '.join(authors)

            # if len(authors_str) > 50:
            #     authors_str = authors_str[:50] + '...'

            # Обработка языков (может быть списком или строкой)
            languages = book.get('languages', [])
            if isinstance(languages, list):
                languages_str = ', '.join(languages)
            else:
                languages_str = str(languages).replace(',', ', ')

            books.append({
                'id': book.get('id', ''),
                'title': book.get('title', ''),
                'author': authors_str,
                'path': '',
                'publisher': book.get('publisher', ''),
                'series': book.get('series', ''),
                'series_index': book.get('series_index', ''),
                'text': book.get('comments', ''),
                'tags': tags_str,
                'languages': languages_str,
                'formats': book.get('formats', '').split(',')
                    if isinstance(book.get('formats'), str)
                    else book.get('formats', []),
                'size': book.get('size', '')
            })

        return books

    except subprocess.CalledProcessError as e:
        logger.error("Ошибка выполнения calibredb: %s", {e.stderr})
        return []
    except json.JSONDecodeError as e:
        logger.error("Ошибка парсинга JSON: %s", {str(e)})
        return []


def search_books(query, search_type='all'):
    """Поиск книг в базе данных Calibre"""
    logger.debug("search_books() start")
    return search_books_calibredb(query, search_type)
