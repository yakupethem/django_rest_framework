from rest_framework.generics import CreateAPIView,ListAPIView,UpdateAPIView,RetrieveAPIView

from comment.api.paginations import CommentPagination
from comment.api.permissions import IsOwner
from comment.api.serializers import CreateCommentSerializers,CommentListSerializer,CommenUpdateDeleteSerializer
from comment.models import Comment

from rest_framework.mixins import DestroyModelMixin

class CreateCommentAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CreateCommentSerializers

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class CreateListAPIView(ListAPIView):
    serializer_class = CommentListSerializer
    pagination_class = CommentPagination

    def get_queryset(self):
        queryset = Comment.objects.filter(parent=None)
        query = self.request.GET.get("q")
        if query:
            queryset=queryset.filter(post=query)
        return queryset


class UpdateCommentAPIView(UpdateAPIView,RetrieveAPIView,DestroyModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommenUpdateDeleteSerializer
    lookup_field = "pk"
    permission_classes = [IsOwner]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)