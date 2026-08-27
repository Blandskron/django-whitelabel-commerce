# Flujo de carrito y pedido

## Carrito

1. Un POST a `cart:add` recibe producto y cantidad con CSRF.
2. La vista convierte y valida la cantidad; comprueba stock según la tienda.
3. `Cart` guarda solo ID y cantidad en `request.session["cart"]`.
4. Al iterar consulta productos activos y calcula subtotales con el precio actual.

Una sesión antigua puede apuntar a un producto desactivado; el iterador lo omite
y `is_empty` cuenta solo elementos comprables.

## Checkout

```text
GET  → formulario vacío o datos iniciales del usuario → checkout.html
POST → CheckoutForm.is_valid()
     → cleaned_data
     → transaction.atomic + bloqueo de productos
     → Order + OrderItem + descuento de stock
     → limpiar carrito
     → guardar acceso de invitado en sesión
     → redirect a orders:order_detail
```

Si el stock cambió entre carrito y POST, el servicio lanza
`InsufficientStockError`, no crea datos parciales y devuelve al carrito. Si el
administrador habilita venta sin stock, el pedido se permite y el inventario no
baja de cero.

`OrderItem.product_name`, `unit_price` y `line_total` son snapshots: un pedido
histórico no cambia cuando se edita el catálogo. `build_whatsapp_url()` usa esos
snapshots y codifica el texto en una URL `wa.me`.
