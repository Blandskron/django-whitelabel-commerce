# Testing

Ejecuta toda la suite:

```bash
python manage.py test
```

O una parte mientras trabajas:

```bash
python manage.py test apps.cart
python manage.py test apps.orders.tests.CheckoutTests
```

Los tests usan una base temporal en memoria; no modifican `db.sqlite3`. La suite
enseña `TestCase`, `setUpTestData`, cliente HTTP, sesión, redirects, comandos de
management e invariantes persistentes.

Antes de terminar un cambio ejecuta también:

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
```

Un test útil expresa comportamiento observable. Evita probar detalles internos
sin valor, repetir el framework o cambiar expectativas solo para ocultar un bug.
