# django-whitelabel-commerce

Base ecommerce white label para pymes: catalogo, carrito por sesion, checkout,
pedido interno y cierre por WhatsApp con gestion manual desde Django Admin.

## Instalacion local

Instalar dependencias:

```powershell
pip install -r requirements.txt
```

Crear base de datos inicial SQLite:

```powershell
python manage.py migrate
```

Crear superusuario y levantar servidor:

```powershell
python manage.py createsuperuser
python manage.py collectstatic --noinput
python manage.py runserver
```

Abrir:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/admin/
https://ecommerce.blandskron.com/
```

## Modulos

```text
apps/
|-- core
|-- common
|-- branding
|-- storefront
|-- catalog
|-- cart
|-- orders
|-- customers
`-- admin_panel
```

## Flujo implementado

- Configuracion de tienda desde `branding.StoreSettings`.
- Productos, categorias e imagenes desde el admin.
- Home, listado, detalle de producto y contacto con templates Django.
- Carrito basado en sesiones.
- Checkout sin cuenta obligatoria.
- Pedido con codigo humano `PED-YYYYMMDD-000001`.
- Snapshot de producto, cantidad y precio en `OrderItem`.
- Link de WhatsApp con mensaje prellenado.
- Estados de pedido y pago editables desde Django Admin.
