from django.contrib import admin

from apps.orders.models import Order, OrderItem, OrderStatus, PaymentStatus


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "product_name", "unit_price", "quantity", "line_total")
    can_delete = False


@admin.action(description="Marcar como pagado")
def mark_as_paid(modeladmin, request, queryset):
    queryset.update(payment_status=PaymentStatus.PAID)


@admin.action(description="Marcar como confirmado")
def mark_as_confirmed(modeladmin, request, queryset):
    queryset.update(status=OrderStatus.CONFIRMED)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("code", "customer_name", "customer_phone", "status", "payment_status", "total", "created_at")
    list_filter = ("status", "payment_status", "created_at")
    search_fields = ("code", "customer_name", "customer_phone", "customer_email")
    readonly_fields = ("code", "subtotal", "total", "created_at", "updated_at")
    inlines = [OrderItemInline]
    actions = [mark_as_paid, mark_as_confirmed]
    fieldsets = (
        ("Pedido", {"fields": ("code", "status", "payment_status", "subtotal", "total")}),
        ("Cliente", {"fields": ("user", "customer_name", "customer_phone", "customer_email")}),
        ("Entrega", {"fields": ("shipping_address", "customer_note")}),
        ("Fechas", {"fields": ("created_at", "updated_at")}),
    )

# Register your models here.
