from rest_framework.generics import ListAPIView,RetrieveUpdateAPIView,CreateAPIView,RetrieveAPIView,DestroyAPIView,UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter,SearchFilter

from post.api.paginations import PostPagination
from post.api.permissions import IsOwner
from post.api.serializers import PostSerialiers
from post.models import Post



class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerialiers
    search_fields=["title","content"]
    filter_backends = [SearchFilter,OrderingFilter]
    pagination_class = PostPagination


class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerialiers
    lookup_field = "slug"
class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerialiers
    lookup_field = "slug"
    permission_classes = [IsOwner]

class PostUpdatelAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerialiers
    lookup_field = "slug"
    permission_classes = [IsOwner]

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)

class PostCreatelAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerialiers
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

