from rest_framework.decorators import api_view
from rest_framework.response import Response

from applications.product.models import Product
from applications.product.serializers.product_serializers import ProductSerializer


@api_view(["GET"])
def get_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_product(request, pk):
    product = Product.objects.get(_id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)
