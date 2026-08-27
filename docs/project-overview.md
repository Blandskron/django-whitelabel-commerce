# Visión general

White Label Commerce es una tienda server-rendered para aprender Django mediante
un caso completo pero acotado. Una sola instalación representa una marca; el
administrador cambia nombre, colores, contacto, catálogo y reglas de stock.

## Recorrido sugerido

1. Ejecuta migraciones y `seed_demo`.
2. Navega home, categorías y detalle de producto.
3. Observa la sesión después de agregar un producto.
4. Sigue el ciclo GET/POST de `CheckoutForm`.
5. Compara `Product` con el snapshot `OrderItem`.
6. Entra al admin y cambia marca, stock y estados.
7. Ejecuta tests individuales y provoca una validación fallida.
8. Repite el laboratorio dentro de Docker.

## Límites intencionales

No hay pasarela de pago, cálculo de despacho, API REST ni multi-tenancy dentro de
una base. “White-label” significa que cada despliegue configura una tienda. El
cierre por WhatsApp y la gestión de pagos son manuales para mantener el foco en
fundamentos Django.
