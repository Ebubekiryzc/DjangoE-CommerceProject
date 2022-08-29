from django.urls import path
from . import views
from . import helpers

urlpatterns = [
    path("", views.get_users, name='users'),
    path("login/", helpers.CustomTokenObtainPairView.as_view(),
         name="token_obtain_pair"),
    path("profile/", views.get_user_profile, name='user-profile'),
    path("register/", views.register_user, name='register'),
]
