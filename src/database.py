"""Функции для работы с базой"""
import os
import subprocess
import json
import shlex
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

    # Базовые параметры команды
    base_cmd = [
        'calibredb', 'list',
        '--with-library', CALIBRE_LIBRARY_URL,
        '--username', CALIBRE_LIBRARY_USER,
        '--password', CALIBRE_LIBRARY_PASS,
        '--for-machine',
        '--limit', str(BOOKS_LIMIT_COUNT),
        '--fields',
        'authors,title,languages,tags,comments,series,series_index,size,formats,publisher',
        '--sort-by', 'series,series_index,title,author_sort,pubdate'
    ]

    # Добавляем параметры поиска в зависимости от типа
    if search_type == 'title':
        base_cmd.extend(['--search', f'title:{query}'])
    elif search_type == 'author':
        base_cmd.extend(['--search', f'authors:{query}'])
    elif search_type == 'series':
        base_cmd.extend(['--search', f'series:{query}'])
    elif search_type == 'id':
        base_cmd.extend(['--search', f'id:{query}'])
    elif search_type == 'random':
        base_cmd.extend(['--limit', f'{RANDOM_BOOKS_COUNT}'])  # Для случайных книг
        base_cmd.extend(['--sort-by', 'random()'])
    else:
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

            # Обработка авторов (может быть строкой с разделителями &)
            authors = book.get('authors', '')
            if isinstance(authors, str):
                authors_str = authors.replace('&', ', ')
            else:
                authors_str = ', '.join(authors)

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
