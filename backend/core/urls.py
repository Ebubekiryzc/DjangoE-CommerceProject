from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views
from applications.product.views import order_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/routes', views.get_routes, name="routes"),
    path("api/products/", include("applications.product.urls.product_urls")),
    path("api/orders/", include("applications.product.urls.order_urls")),
    path("api/users/", include("applications.account.urls")),
    path("api/webhook/", order_views.stripe_webhook_view, name="stripe-webhook")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
