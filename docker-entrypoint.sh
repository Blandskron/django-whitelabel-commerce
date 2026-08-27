#!/bin/sh
set -e

echo "Aplicando migraciones..."
python manage.py migrate --noinput

echo "Recolectando archivos estaticos..."
python manage.py collectstatic --noinput

case "${DJANGO_CREATE_SUPERUSER:-False}" in
  True|true|1|yes)
    echo "Comprobando superusuario educativo..."
    python manage.py ensure_superuser
    ;;
esac

exec "$@"
