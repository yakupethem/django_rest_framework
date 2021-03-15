from rest_framework.generics import CreateAPIView,ListAPIView,DestroyAPIView,UpdateAPIView,RetrieveAPIView

from comment.api.paginations import CommentPagination
from comment.api.permissions import IsOwner
from comment.api.serializers import CreateCommentSerializers,CommentListSerializer,CommenUpdateDeleteSerializer
from comment.models import Comment

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

class DeleteCommentAPIView(DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommenUpdateDeleteSerializer
    lookup_field = "pk"
    permission_classes = [IsOwner]

class UpdateCommentAPIView(UpdateAPIView,RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommenUpdateDeleteSerializer
    lookup_field = "pk"
    permission_classes = [IsOwner]