from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from applications.product.models import Product, Order, OrderItem
from applications.product.serializers.product_serializers import ProductSerializer
from applications.product.models import ShippingAddress
from applications.product.serializers.order_serializers import OrderSerializer

from datetime import datetime

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


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


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_my_orders(request):
    user = request.user
    orders = user.order_set.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_order_by_id(request, pk):
    user = request.user
    try:
        order = Order.objects.get(_id=pk)
        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            return Response({"detail": "Not authorized to view this order"},
                            status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"detail": "Order does not exist"}, status=status.HTTP_400_BAD_REQUEST)


def update_order_to_paid(pk):
    order = Order.objects.get(_id=pk)

    order.isPaid = True
    order.paidAt = datetime.now()
    order.save()


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def pay_order(request, pk):
    order = Order.objects.get(_id=pk)
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(order.totalPrice * 100),
                        "product_data": {
                            "name": "Order"
                        }
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                "order_id": order._id
            },
            payment_method_types=[
                "card",
            ],
            mode="payment",
            success_url=f"{settings.SITE_URL}/order/{order._id}" + \
            "?success=true",
            cancel_url=f"{settings.SITE_URL}/order/{order._id}" + \
            "?cancelled=true"
        )
        return Response(checkout_session.url)
    except Exception as e:
        print(e)
        return Response({"detail": "Something went wrong while creating stripe session"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEB_HOOK_SECRET_KEY
        )
    except ValueError as e:
        return Response(status=400)
    except stripe.error.SignatureVerificationError as e:
        return Response(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        order_id = session["metadata"]["order_id"]
        update_order_to_paid(order_id)

        customer_email = session['customer_details']['email']

        send_mail(
            subject="Payment Sucessful",
            message=f"Thank for your purchase your order is ready.",
            recipient_list=[customer_email],
            from_email=settings.EMAIL_HOST_USER
        )

    return HttpResponse(status=200)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def get_orders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAdminUser])
def update_order_to_delivered(request, pk):
    order = Order.objects.get(_id=pk)

    order.isDelivered = True
    order.deliveredAt = datetime.now()
    order.save()

    return Response("Order was delivered")
