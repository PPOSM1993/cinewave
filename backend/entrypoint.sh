#!/bin/bash

echo "📦 Esperando base de datos..."
while ! nc -z db 5432; do
  sleep 1
done

echo "✅ Base de datos conectada."

python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:8000
