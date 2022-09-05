from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from applications.product.models import Product, Review
from applications.product.serializers.product_serializers import ProductSerializer


@api_view(["GET"])
def get_products(request):
    query = request.query_params.get("keyword")
    if query == None:
        query = ""

    products = Product.objects.filter(name__icontains=query)

    page = request.query_params.get("page")
    paginator = Paginator(products, 2)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)

    serializer = ProductSerializer(products, many=True)
    return Response({"products": serializer.data, "page": page, "pages": paginator.num_pages})


@api_view(["GET"])
def get_product(request, pk):
    product = Product.objects.get(_id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def delete_product(request, pk):
    product = Product.objects.get(_id=pk)
    product.delete()
    return Response("Product Deleted")


@api_view(["POST"])
@permission_classes([IsAdminUser])
def create_product(request):
    user = request.user
    product = Product.objects.create(
        user=user,
        name="Sample name",
        price=0,
        brand="Sample brand",
        category="SampleCategory",
        countInStock=0,
        description=""
    )

    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAdminUser])
def update_product(request, pk):
    data = request.data
    product = Product.objects.get(_id=pk)

    product.name = data["name"]
    product.price = data["price"]
    product.brand = data["brand"]
    product.countInStock = data["countInStock"]
    product.category = data["category"]
    product.description = data["description"]

    product.save()

    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(["POST"])
def upload_image(request):
    data = request.data
    productId = data["product_id"]
    product = Product.objects.get(_id=productId)

    product.image = request.FILES.get("image")
    product.save()
    return Response("Image was uploaded.")


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_product_review(request, pk):
    user = request.user
    product = Product.objects.get(_id=pk)
    data = request.data

    # (1) Review already exist
    alreadyExist = product.review_set.filter(user=user).exists()

    if alreadyExist:
        content = {"detail": "Product already reviewed"}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # (2) No Rating or 0
    elif data["rating"] == 0:
        content = {"detail": "Please select a rating"}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # (3) Create review
    else:
        review = Review.objects.create(
            user=user,
            product=product,
            name=user.first_name,
            rating=data["rating"],
            comment=data["comment"]
        )

        reviews = product.review_set.all()
        product.numReviews = len(reviews)

        total = 0
        for review in reviews:
            total += review.rating

        product.rating = total / len(reviews)
        product.save()

        return Response({"detail": "Review added"})
