from django.urls import path
from applications.product.views import order_views
from applications.product.views.order_views import get_order_by_id
from backend.applications.product.views.order_views import update_order_to_paid

urlpatterns = [
    path("add/", order_views.add_order_items, name="orders-add"),
    path("<str:pk>/", order_views.get_order_by_id, name="user-order"),
    path("<str:pk>/pay/", order_views.update_order_to_paid, name="pay-order")
]
