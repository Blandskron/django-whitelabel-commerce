# Django White Label Commerce

Tienda educativa adaptable para pequeñas empresas. Incluye catálogo, carrito en
sesión, checkout, pedidos internos, confirmación por WhatsApp y gestión mediante
Django Admin. Está diseñada como laboratorio para aprender el recorrido completo
de una petición web sin ocultarlo detrás de dependencias o capas innecesarias.

## Qué aprenderás

- cómo se conectan URL, vista, modelo, formulario y template;
- relaciones `ForeignKey`, modelos abstractos y snapshots de datos;
- sesiones, mensajes, autenticación y autorización básica;
- transacciones y control de stock durante un checkout;
- personalización de Django Admin;
- comandos de administración idempotentes, tests y Docker.

## Funcionalidades

- marca, colores, contacto y reglas de venta configurables;
- categorías, productos, galería, stock y destacados;
- carrito sin cuenta, guardado en la sesión del navegador;
- registro, login e historial de pedidos para clientes;
- checkout como invitado o usuario autenticado;
- enlace de WhatsApp con el resumen del pedido;
- panel administrativo con filtros, búsquedas y acciones masivas.

## Tecnologías y requisitos

- Python 3.12 recomendado (Django 5.2 soporta Python 3.10 o superior);
- Django 5.2 LTS, SQLite, HTML y CSS;
- Pillow, django-environ y WhiteNoise;
- Gunicorn dentro de Docker;
- Git y, opcionalmente, Docker Desktop con Compose.

## Instalación local

```bash
git clone https://github.com/Blandskron/django-whitelabel-commerce.git
cd django-whitelabel-commerce
python -m venv .venv
```

Activa el entorno virtual:

```bash
# Linux/macOS
source .venv/bin/activate

# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

Instala y configura:

```bash
pip install -r requirements.txt
cp .env.example .env                    # Linux/macOS
Copy-Item .env.example .env             # Windows PowerShell (alternativa)
python manage.py migrate
python manage.py seed_demo
```

Antes de compartir o desplegar, reemplaza `DJANGO_SECRET_KEY` y
`DJANGO_SUPERUSER_PASSWORD` en `.env`. El archivo `.env` está ignorado por Git.

Inicia la aplicación:

```bash
python manage.py runserver
```

Visita <http://127.0.0.1:8000/> y <http://127.0.0.1:8000/admin/>.

## Superusuario y datos iniciales

La opción interactiva estándar siempre está disponible:

```bash
python manage.py createsuperuser
```

Para clases o Docker, `ensure_superuser` lee las variables
`DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL` y
`DJANGO_SUPERUSER_PASSWORD`. Es idempotente: no duplica el usuario existente.

```bash
python manage.py ensure_superuser
python manage.py seed_demo
```

`seed_demo` también es idempotente y crea dos categorías y cuatro productos. En
el admin puedes editar esos datos, configurar la tienda y revisar pedidos.

## Docker

Copia primero el ejemplo de entorno si quieres crear el administrador educativo
automáticamente. Después ejecuta:

```bash
docker compose up --build
```

El entrypoint aplica migraciones, ejecuta `collectstatic`, crea el superusuario
solo cuando `DJANGO_CREATE_SUPERUSER=True` y finalmente inicia Gunicorn. SQLite y
los uploads viven en volúmenes Docker.

```bash
docker compose exec web python manage.py seed_demo
docker compose exec web python manage.py test
docker compose down
docker compose down -v   # reinicio total: elimina base y uploads de Docker
```

`down -v` elimina datos locales de los volúmenes; úsalo solo cuando realmente
quieras comenzar desde cero.

## Tests y verificaciones

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
docker compose config
```

Las pruebas cubren configuración de marca, catálogo, cantidades del carrito,
stock transaccional, privacidad del pedido, comandos idempotentes y páginas
públicas. Consulta [docs/testing.md](docs/testing.md).

## Estructura

```text
.
├── apps/
│   ├── branding/       # configuración white-label
│   ├── cart/           # carrito almacenado en sesión
│   ├── catalog/        # categorías, productos e imágenes
│   ├── common/         # timestamps y comandos educativos
│   ├── customers/      # registro, login y perfil
│   ├── orders/         # checkout, pedidos y stock
│   └── storefront/     # home y contacto
├── config/             # settings, URLs y entrypoints WSGI/ASGI
├── docs/               # guías de estudio y estado del proyecto
├── static/             # CSS fuente
├── templates/          # templates globales e includes
├── Dockerfile
├── compose.yaml
├── docker-entrypoint.sh
├── manage.py
└── requirements.txt
```

## Flujo educativo

```text
Navegador → URL nombrada → View → Model / Form / Service → Template → Response
                              ↘ sesión, mensajes y transacción ↗
```

Ejemplo: `checkout/` resuelve `orders:checkout`; la vista valida
`CheckoutForm`; el servicio crea `Order` y `OrderItem` dentro de una transacción;
la respuesta redirige al detalle autorizado del pedido.

## Documentación

- [visión general](docs/project-overview.md);
- [arquitectura](docs/architecture.md) y [responsabilidad de apps](docs/apps.md);
- [flujo de pedido](docs/order-flow.md);
- [guía del admin](docs/admin-guide.md);
- [testing](docs/testing.md), [troubleshooting](docs/troubleshooting.md) y
  [próximos pasos](docs/roadmap.md);
- [estado para continuidad](docs/PROJECT_STATUS.md).

## Desarrollo frente a producción

`.env.example` prioriza desarrollo educativo (`DEBUG=True`, HTTP y una
contraseña demostrativa que debes cambiar). No copies esos valores a producción.
En producción usa una clave aleatoria, HTTPS, cookies seguras, hosts/orígenes
reales y una base de datos y estrategia de backups apropiadas. WhiteNoise usa un
manifiesto de archivos estáticos cuando `DEBUG=False`.
