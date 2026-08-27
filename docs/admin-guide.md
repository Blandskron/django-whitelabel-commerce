# Guía de Django Admin

Accede a <http://127.0.0.1:8000/admin/> con un superusuario. Puedes crearlo con
`createsuperuser` o con el comando idempotente `ensure_superuser` descrito en el
README.

## Orden recomendado

1. **Configuración de tienda**: nombre, colores, textos, moneda y WhatsApp. Solo
   se permite un registro.
2. **Categorías**: nombre, orden y visibilidad.
3. **Productos**: precio, stock, destacado, estado e imágenes inline.
4. **Pedidos**: filtra por estado/pago, busca por código o cliente y revisa items.
5. Usa las acciones “Marcar como pagado” y “Marcar como confirmado” con cuidado.

Los campos de totales, código, snapshots y fechas son de solo lectura porque se
generan durante el checkout. El admin es una herramienta interna, no una vista
para compradores.

Error común: crear el producto pero dejarlo inactivo o sin stock. En ese caso no
se podrá comprar salvo que la configuración permita pedidos sin stock.
