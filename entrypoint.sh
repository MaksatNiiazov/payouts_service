#!/bin/sh
set -e

echo "Waiting for database..."
while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 1
done
echo "Database is up"

if [ "$RUN_MIGRATIONS" = "1" ]; then
  echo "Applying migrations..."
  python manage.py migrate --noinput
fi

if [ "$DJANGO_DEBUG" = "0" ] && [ "$RUN_COLLECTSTATIC" = "1" ]; then
  echo "Collect static..."
  python manage.py collectstatic --noinput
fi

exec "$@"
