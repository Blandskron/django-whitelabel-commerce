# Guía para agentes y colaboradores

## Objetivo

Proyecto educativo Django 5.2 para estudiar una tienda white-label. Mantener
Django idiomático, explícito y proporcional: no introducir APIs, colas,
microservicios o nuevas capas sin un requisito concreto.

## Antes de modificar

1. Leer `README.md`, `docs/architecture.md` y `docs/PROJECT_STATUS.md`.
2. Revisar la app afectada completa: modelo, migraciones, vista, URL, template,
   admin y tests.
3. Preservar ejecución local y Docker con SQLite.
4. No borrar migraciones históricas ni editar secretos reales.
5. No modificar uploads de `media/` salvo que la tarea los incluya.

## Mapa rápido

- `config/settings.py`: entorno, base de datos, estáticos y seguridad.
- `apps/catalog/`: catálogo persistente.
- `apps/cart/cart.py`: carrito en sesión; no posee tablas.
- `apps/orders/services.py`: transacción de checkout y WhatsApp.
- `apps/branding/`: singleton con configuración de la tienda.
- `apps/common/management/commands/`: seed y superusuario educativo.
- `templates/base.html`: herencia principal; `static/css/site.css`: estilos.
- `docker-entrypoint.sh`: migraciones, estáticos e inicialización opcional.

## Comandos esenciales

```bash
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
docker compose config
docker compose up --build
```

Se necesita un `.env` basado en `.env.example` para ejecución local. Nunca se
versiona `.env`, `db.sqlite3`, `staticfiles/`, nuevos uploads ni caches.

## Reglas de cambio

- Toda URL interna debe ser nombrada y resolverse con `reverse` o `{% url %}`.
- Todo POST desde template debe incluir CSRF.
- Validaciones de entrada pertenecen a forms o al borde de la vista; invariantes
  de checkout también se revalidan dentro de la transacción.
- El carrito conserva IDs y cantidades; no serializar objetos Django en sesión.
- `OrderItem` conserva el snapshot histórico aunque cambie o se elimine producto.
- Los comandos repetibles deben ser idempotentes.
- Un cambio de modelo exige migración nueva; nunca reescribir `0001_initial.py`.
- Agregar tests de comportamiento para correcciones o funcionalidad nueva.

## Criterio mínimo de terminado

Ejecutar y registrar resultados reales de:

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
docker compose config
```

Si cambia Docker, intentar también `docker compose build`. Revisar `git diff`,
buscar secretos y mantener README, docs y `PROJECT_STATUS.md` sincronizados.
