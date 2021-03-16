from django.urls import path
from comment.api.views import CreateCommentAPIView,CreateListAPIView,UpdateCommentAPIView

app_name="comment"

urlpatterns=[
    path("create",CreateCommentAPIView.as_view(),name="create"),
    path("list",CreateListAPIView.as_view(),name="list"),
    path("update/<pk>",UpdateCommentAPIView.as_view(),name="update")

]