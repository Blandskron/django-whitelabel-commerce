# Próximos pasos de aprendizaje

Orden sugerido, sin convertir el laboratorio en una plataforma empresarial:

1. Añadir validación de teléfono en `CheckoutForm` y sus tests.
2. Crear filtros de catálogo por texto o categoría usando parámetros GET.
3. Probar permisos del historial para usuarios autenticados.
4. Agregar una transición validada de estados del pedido.
5. Incorporar una fixture alternativa y comparar con `seed_demo`.
6. Practicar una migración añadiendo SKU único a `Product`.
7. Configurar CI sencillo con `check`, migraciones y tests.

Antes de una producción real aún harían falta decisiones de negocio: pagos,
despacho, impuestos, backups, observabilidad, PostgreSQL y almacenamiento durable
de media. No deben añadirse hasta que un requisito concreto lo justifique.
