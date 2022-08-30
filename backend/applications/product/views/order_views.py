from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from applications.product.models import Product, Order, OrderItem
from applications.product.serializers.product_serializers import ProductSerializer
from applications.product.models import ShippingAddress
from applications.product.serializers.order_serializers import OrderSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_order_items(request):
    user = request.user
    data = request.data
    orderItems = data["orderItems"]
    if orderItems and len(orderItems) == 0:
        return Response({"detail": "No order items"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        # (1) Create order
        order = Order.objects.create(
            user=user,
            paymentMethod=data["paymentMethod"],
            taxPrice=data["taxPrice"],
            shippingPrice=data["shippingPrice"],
            totalPrice=data["totalPrice"],
        )

        # (2) Create shipping address
        shipping = ShippingAddress.objects.create(
            order=order,
            address=data["shippingAddress"]["address"],
            city=data["shippingAddress"]["city"],
            postalCode=data["shippingAddress"]["postalCode"],
            country=data["shippingAddress"]["country"]
        )

        # (3) Create order items and set order to orderItem relationship
        for i in orderItems:
            product = Product.objects.get(_id=i["product"])

            item = OrderItem.objects.create(
                product=product,
                order=order,
                name=product.name,
                quantity=i["quantity"],
                price=i["price"],
                image=product.image.url
            )

            # (3.1) Update stock

            product.countInStock -= item.quantity
            product.save()
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)
