from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def get_routes(request):
    routes = [
        "/api/products/",
        "/api/products/create/",

        "/api/products/upload/",

        "/api/products/<id>/reviews/",

        "/api/products/top/",
        "/api/products/<id>/",

        "/api/products/delete/<id>/",
        "/api/products/<update>/<id>/",
    ]
    return Response(routes)
