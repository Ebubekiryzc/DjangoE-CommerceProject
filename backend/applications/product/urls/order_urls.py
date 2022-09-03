from django.urls import path
from applications.product.views import order_views

urlpatterns = [
    path("add/", order_views.add_order_items, name="orders-add"),
    path("<str:pk>/", order_views.get_order_by_id, name="user-order"),
    path("<str:pk>/pay/", order_views.pay_order, name="pay-order")
]
