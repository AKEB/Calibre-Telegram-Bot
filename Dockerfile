
FROM ghcr.io/linuxserver/calibre:latest

# Установка необходимых системных зависимостей
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip python3.12-venv && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p /app/src && \
    mkdir -p /app/tests && \
    mkdir -p /app/config && \
    touch /app/config/authorized_users.txt

# Создать рабочую директорию
WORKDIR /app
# Переменные окружения
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=./

RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

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
ENTRYPOINT []
CMD ["python", "/app/src/main.py"]
