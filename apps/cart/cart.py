from apps.catalog.models import Product


class Cart:
    session_key = "cart"

    def __init__(self, request):
        self.session = request.session
        self.data = self.session.get(self.session_key, {})

    def add(self, product, quantity=1, replace=False):
        product_id = str(product.id)
        current = self.data.get(product_id, 0)
        self.data[product_id] = int(quantity) if replace else current + int(quantity)
        if self.data[product_id] <= 0:
            self.data.pop(product_id, None)
        self.save()

    def remove(self, product_id):
        self.data.pop(str(product_id), None)
        self.save()

    def clear(self):
        self.session[self.session_key] = {}
        self.session.modified = True
        self.data = {}

    def save(self):
        self.session[self.session_key] = self.data
        self.session.modified = True

    def __iter__(self):
        products = Product.objects.filter(id__in=self.data.keys(), is_active=True)
        product_map = {str(product.id): product for product in products}
        for product_id, quantity in self.data.items():
            product = product_map.get(product_id)
            if not product:
                continue
            line_total = product.price * quantity
            yield {
                "product": product,
                "quantity": quantity,
                "unit_price": product.price,
                "line_total": line_total,
            }

    def __len__(self):
        # Cuenta solo productos que todavía existen y están publicados. Así una
        # sesión antigua no muestra unidades que ya no pueden comprarse.
        return sum(item["quantity"] for item in self)

    @property
    def items(self):
        return list(self)

    @property
    def subtotal(self):
        return sum(item["line_total"] for item in self)

    @property
    def total(self):
        return self.subtotal

    @property
    def is_empty(self):
        return len(self) == 0
