from django.urls import path,include

from post.api.views import PostListAPIView,PostCreatelAPIView,PostDetailAPIView,PostDeleteAPIView,PostUpdatelAPIView

urlpatterns = [
    path("list",PostListAPIView.as_view(),name="list"),
    path("detail/<slug>",PostDetailAPIView.as_view(),name="detail"),
    path("delete/<slug>",PostDeleteAPIView.as_view(),name="delete"),
    path("update/<slug>",PostUpdatelAPIView.as_view(),name="update"),
    path("create",PostCreatelAPIView.as_view(),name="create")
]
