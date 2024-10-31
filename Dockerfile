FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y vim postgresql-client && \
    rm -rf /var/lib/apt/lists/*

COPY . .
# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
# Копирование и предоставление прав на выполнение скрипта запуска
COPY startup.sh /app/startup.sh
RUN chmod +x /app/startup.sh

CMD ["/app/startup.sh"]