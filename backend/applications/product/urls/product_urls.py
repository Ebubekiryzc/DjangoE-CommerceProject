from django.urls import path
from applications.product.views import product_views

urlpatterns = [
    path("", product_views.get_products, name="products"),
    path("<str:pk>/", product_views.get_product, name="product")
]
