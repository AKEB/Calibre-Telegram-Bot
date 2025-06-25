# Calibre Telegram Bot

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
