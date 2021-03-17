from django.urls import path
from account.api.views import ProfileView,UpdatePasswor,CreateUserViev

app_name="account"

urlpatterns=[
    path("me",ProfileView.as_view(),name="me"),
    path("changepassword",UpdatePasswor.as_view(),name="changepassword"),
    path("register",CreateUserViev.as_view(),name="register"),
]