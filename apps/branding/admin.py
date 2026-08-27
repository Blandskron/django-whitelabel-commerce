from django.contrib import admin

from apps.branding.models import StoreSettings


@admin.register(StoreSettings)
class StoreSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Marca", {"fields": ("store_name", "logo", "favicon", "primary_color", "secondary_color")}),
        ("Landing", {"fields": ("hero_title", "hero_subtitle")}),
        ("Contacto", {"fields": ("whatsapp_number", "contact_email", "instagram_url", "facebook_url", "address")}),
        ("Venta", {"fields": ("bank_details", "currency", "show_stock", "allow_out_of_stock_orders")}),
        ("Operacion", {"fields": ("maintenance_mode",)}),
    )

    def has_add_permission(self, request):
        return not StoreSettings.objects.exists()
