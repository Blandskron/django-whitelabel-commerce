# Arquitectura

La aplicación usa el patrón MTV de Django y templates renderizados en servidor.
`config/urls.py` delega cada prefijo a la app correspondiente. Las vistas de
negocio son function-based views; login/logout reutilizan class-based views
incluidas en Django porque allí reducen duplicación sin ocultar lógica propia.

```text
HTTP request
  → config/urls.py
  → apps/<dominio>/urls.py
  → view
      → form (entrada)
      → model/queryset o service (datos y transacción)
      → messages/session (estado temporal)
  → template que extiende base.html
  → HTTP response o redirect nombrado
```

## Datos

- SQLite es el valor local y Docker: suficiente para el nivel del laboratorio.
- `TimeStampedModel` aporta fechas a modelos persistentes.
- `Category → Product → ProductImage` modela el catálogo.
- `Order → OrderItem` conserva el detalle comprado.
- `Order.user` es opcional: admite checkout invitado y cuenta registrada.
- `StoreSettings` es un singleton lógico administrado con `load()`.
- `Cart` no es modelo: serializa `{product_id: quantity}` en la sesión.

## Límites y seguridad

El stock se valida al editar el carrito y otra vez dentro de una transacción con
`select_for_update()` al crear el pedido. Un invitado solo puede volver a su
pedido desde la misma sesión; usuario dueño y staff también tienen acceso. Las
URLs `next` se validan para impedir redirecciones externas.

WhiteNoise sirve estáticos. Con `DEBUG=True` se usa almacenamiento simple para
que `runserver` y tests no dependan de `collectstatic`; con `DEBUG=False` se usa
manifiesto comprimido y el entrypoint lo genera antes de Gunicorn.
