# Estado del proyecto

Actualizado: 2026-08-27.

## Estado actual

Laboratorio funcional con catálogo, carrito por sesión, cuentas, checkout,
pedidos, WhatsApp, admin, datos demo, tests y ejecución local/Docker.

## Decisiones

- Django server-rendered y SQLite para mantener el foco educativo.
- Function-based views para negocio; auth reutiliza vistas Django.
- Transacción y bloqueo de productos al cerrar pedido.
- Acceso de invitado a pedido limitado a su sesión.
- Un proceso Docker; no se añade PostgreSQL sin necesidad didáctica.

## Validación requerida

`check`, `makemigrations --check --dry-run`, `test` y `docker compose config`.
Consultar el último commit o informe de entrega para resultados ejecutados.

## Última validación

- `python manage.py check`: OK, sin incidencias.
- `python manage.py makemigrations --check --dry-run`: OK, sin cambios.
- `python manage.py test`: OK, 17 tests.
- `docker-compose -f compose.yaml config`: OK.
- Build/arranque Docker: no confirmado; el cliente del host quedó bloqueado al
  conectar con Docker Desktop y se detuvo sin atribuirle un resultado exitoso.

## Problemas conocidos

- Un ZIP histórico incluía un `.env` real. El artefacto fue retirado del árbol,
  pero la clave debe rotarse en el entorno donde se haya usado; el historial no
  se reescribe porque el flujo prohíbe force push.
- El repositorio no declara todavía una licencia de distribución. El propietario
  debe elegirla antes de presentarlo como proyecto open source.
- `maintenance_mode` está disponible en configuración pero aún no intercepta
  peticiones; queda como ejercicio si existe un requisito claro.

## Próximo paso recomendado

Estudiar `apps/orders/services.py`, reproducir el cambio de stock entre carrito y
checkout, y luego añadir validación de teléfono a `CheckoutForm` con sus tests.
