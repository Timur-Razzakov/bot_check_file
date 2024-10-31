#!/bin/sh

# Ожидание готовности базы данных
while ! pg_isready -h "db" -p 5432 --quiet; do
  sleep 1
done

# миграций Alembic
alembic upgrade head

# Запуск
python main.py