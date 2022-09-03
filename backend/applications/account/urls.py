from django.urls import path
from . import views
from . import helpers

urlpatterns = [
    path("", views.get_users, name='users'),
    path("delete/<str:pk>/", views.delete_user, name='delete-user'),
    path("login/", helpers.CustomTokenObtainPairView.as_view(),
         name="token_obtain_pair"),
    path("profile/", views.get_user_profile, name='user-profile'),
    path("profile/update/", views.update_profile, name='update-user-profile'),
    path("register/", views.register_user, name='register'),
]
