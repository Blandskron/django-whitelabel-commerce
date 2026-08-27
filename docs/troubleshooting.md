# Troubleshooting

## `ModuleNotFoundError: No module named 'django'`

**Causa:** entorno virtual inactivo o dependencias no instaladas. **Solución:**
activa `.venv` y ejecuta `pip install -r requirements.txt`.

## Falta `DJANGO_SECRET_KEY`

**Causa:** no existe `.env`. **Solución:** copia `.env.example` a `.env`; no
versiones ese archivo y cambia sus credenciales.

## `no such table` o migraciones pendientes

**Causa:** base nueva o esquema desactualizado. **Solución:**
`python manage.py migrate`. Comprueba con `python manage.py showmigrations`.

## El catálogo está vacío

Ejecuta `python manage.py seed_demo`. Es seguro repetirlo: no duplica los datos
demostrativos que ya existen.

## El superusuario no fue creado en Docker

Comprueba `DJANGO_CREATE_SUPERUSER=True` y las tres variables
`DJANGO_SUPERUSER_*` en `.env`; recrea con `docker compose up` o ejecuta
`docker compose exec web python manage.py ensure_superuser`.

## Puerto 8000 ocupado

Detén el proceso anterior o cambia el mapeo de Compose, por ejemplo
`"8001:8000"`, y abre `http://localhost:8001`.

## Docker daemon no disponible

Inicia Docker Desktop y valida `docker version` antes de `docker compose up`.

## Un producto desapareció del carrito

Fue desactivado o eliminado de la sesión comprable. Reactívalo desde el admin y
verifica su stock. El carrito ignora referencias antiguas deliberadamente.

## Reiniciar Docker desde cero

`docker compose down -v` elimina la base SQLite y uploads de los volúmenes. Es
destructivo para datos locales; después usa `docker compose up --build` y vuelve
a ejecutar `seed_demo`.
