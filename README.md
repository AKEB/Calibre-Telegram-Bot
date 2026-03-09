# Calibre Telegram Bot - App Summary

## What it is

A Telegram bot that connects users to a Calibre library for searching, downloading, and uploading books.
It runs as a polling bot using python-telegram-bot and Calibre command-line/database integrations.

## Who it’s for

Primary persona: an authorized Telegram user who needs fast access to a Calibre collection from chat.
Secondary persona: an admin who grants access and manages user authorization.
Named persona profile: Not found in repo.

## What it does

- Searches books by general query, title, author, series, random selection, or exact ID.
- Shows paginated result cards and lets users pick a book from inline buttons.
- Delivers books in requested format; converts with ebook-convert when needed.
- Uploads books from Telegram documents or URLs into Calibre via calibredb add.
- Enforces authorization and admin-only actions (e.g., adding users).
- Supports per-user language selection (Russian/English) and localized bot text.
- Reports library statistics from the Calibre SQLite metadata database.

## How it works (repo evidence only)

- Entry point: src/main.py validates env config and DB access, builds Application, registers handlers.
- Interface layer: src/handlers.py routes commands/callbacks and manages conversation state.
- Data/services: src/database.py queries via calibredb list and SQLite (random IDs/stats).
- File pipeline: src/download.py reads files/metadata and converts formats; src/upload_file.py ingests Telegram files or URLs and runs calibredb add.
- Auth/localization: src/auth.py stores authorized users + language; src/texts.py + src/i18n/*.yaml format responses.

## How to run (minimal getting started)

1. Prepare env: cp .env.example .env, then set TELEGRAM_BOT_TOKEN, Calibre paths/URLs, and auth settings.
2. Install deps: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt.
3. Start bot: python src/main.py.
4. Optional container path: build Dockerfile and run with mounted /books and /books_import volumes.

Бот для поиска, скачивания и загрузки книг в библиотеку Calibre через Telegram.

## Возможности

- Поиск книг по названию, автору, серии
- Скачивание книг в разных форматах (epub, fb2, mobi, txt, azw3)
- Загрузка новых книг в библиотеку через Telegram
- Статистика библиотеки
- Поддержка авторизации пользователей и администраторов

## Быстрый старт (Docker)

1. Скопируйте `.env.example` и настройте переменные окружения под свои нужды:

   ```sh
   cp .env.example .env
   # отредактируйте .env
   ```

2. Соберите Docker-образ:

   ```sh
   docker build -t calibre-telegram-bot .
   ```

3. Запустите контейнер:

   ```sh
   docker run --rm --env-file .env \
   -v ./src:/app/src/ \
   -v ./tests:/app/tests/ \
   -v ./books:/books \
   -v ./books_import:/books_import \
   -v ./config:/app/config \
   calibre-telegram-bot
   ```

   - `/books` — папка с библиотекой Calibre
   - `/books_import` — папка для загрузки новых книг

## Локальный запуск

1. Установите зависимости:

   ```sh
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Скопируйте и настройте `.env`:

   ```sh
   cp .env.example .env
   # отредактируйте .env
   ```

3. Запустите бота:

   ```sh
   python src/main.py
   ```

## Переменные окружения

- `TELEGRAM_BOT_TOKEN` — токен Telegram-бота
- `CALIBRE_DB` — путь к базе данных Calibre
- `BOOKS_DIR` — папка с книгами
- `BOOKS_IMPORT_DIR` — папка для загрузки новых книг
- `AUTHORIZED_USERS_FILE` — файл с авторизованными пользователями
- `CALIBRE_LIBRARY_URL`, `CALIBRE_LIBRARY_USER`, `CALIBRE_LIBRARY_PASS` — параметры для загрузки книг
- `CALIBRE_WEB_URL` — URL веб-интерфейса Calibre
- `TELEGRAM_ADMIN_USERS` — ID администраторов через запятую

## Тесты

- Для запуска тестов:

  ```sh
  pytest -v tests/
  ```

  ```sh
  docker run -it --rm --env-file .env \
   -v ./src:/app/src/ \
   -v ./tests:/app/tests/ \
   -v ./books:/books \
   -v ./books_import:/books_import \
   -v ./config:/app/config \
   calibre-telegram-bot pytest -v /app/tests/
   ```

## Системные зависимости (для локального запуска)

- calibre
- gcc, libxml2-dev, libxslt1-dev, libffi-dev, libbz2-dev, liblzma-dev, libzstd-dev, libjpeg-dev, libpng-dev, unrar, wget

## Авторы

- @akeb

---
