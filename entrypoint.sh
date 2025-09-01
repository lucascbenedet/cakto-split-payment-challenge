#!/bin/sh
set -e

echo "📌 Esperando o banco ficar pronto..."
while ! nc -z "$DATABASE_HOST" "$DATABASE_PORT"; do
  sleep 1
done

echo "📌 Rodando migrations..."
poetry run python manage.py migrate --noinput

echo "📌 Criando superusuário (se não existir)..."
poetry run python manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.getenv("DJANGO_SUPERUSER_USERNAME")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, password=password, is_superuser=True, is_staff=True)
    print("✅ Superusuário criado:", username)
else:
    print("ℹ️ Superusuário já existe:", username)
EOF

echo "📌 Iniciando Gunicorn..."
exec "$@"
