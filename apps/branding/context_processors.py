from apps.branding.models import StoreSettings


def store_settings(request):
    return {"store_settings": StoreSettings.load()}
