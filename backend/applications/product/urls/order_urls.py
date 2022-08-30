from django.urls import path
from applications.product.views import order_views
from applications.product.views.order_views import get_order_by_id

urlpatterns = [
    path("add/", order_views.add_order_items, name="orders-add"),
    path("<str:pk>/", order_views.get_order_by_id, name="user-order")
]
