# Aplicaciones Django

| App | Responsabilidad | Archivos clave |
| --- | --- | --- |
| `branding` | Configuración única de marca, contacto y venta | `models.py`, `context_processors.py`, `admin.py` |
| `catalog` | Categorías, productos, imágenes y navegación | `models.py`, `views.py`, `urls.py` |
| `cart` | Carrito por sesión y validación inicial de cantidad | `cart.py`, `views.py`, `context_processors.py` |
| `orders` | Formulario, transacción, snapshots y WhatsApp | `forms.py`, `services.py`, `views.py` |
| `customers` | Registro, login, logout y pedidos del usuario | `views.py`, `urls.py` |
| `storefront` | Home y contacto | `views.py`, `urls.py` |
| `common` | Modelo abstracto y comandos compartidos | `models.py`, `management/commands/` |
| `admin_panel` | Títulos globales de Django Admin | `admin.py` |

## Dónde modificar

- Un campo persistente: modelo, migración, admin, form/template y tests.
- Una página nueva: URL nombrada, vista, template y test HTTP.
- Una regla de checkout: `orders/services.py`; no confiar solo en el navegador.
- Navegación o layout: `templates/base.html` e `includes/`.
- Identidad de tienda: `branding.StoreSettings`, no constantes en templates.

Algunas apps conservan `models.py` o `admin.py` pequeños porque son puntos de
extensión estándar de Django. No agregues modelos vacíos para “completar” capas.
