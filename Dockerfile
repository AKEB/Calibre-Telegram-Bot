
FROM ghcr.io/linuxserver/calibre:latest

# Установка необходимых системных зависимостей
RUN mkdir -p /app/src && \
    mkdir -p /app/tests && \
    mkdir -p /app/config && \
    touch /app/config/authorized_users.txt

# Создать рабочую директорию
WORKDIR /app
# Переменные окружения
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=./

# Копировать исходники и requirements
COPY ./requirements.txt ./
# Установить зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src /app/src/
# Проверить код с помощью pylint (ошибка сборки при наличии ошибок)
RUN pylint /app/src/ --fail-under=8

COPY ./tests /app/tests/
# Запустить тесты unittest (ошибка сборки при провале тестов)
RUN pytest -v /app/tests/

# Запуск бота
CMD ["python", "/app/src/main.py"]
