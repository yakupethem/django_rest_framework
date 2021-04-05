from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer,SerializerMethodField
from comment.models import Comment
from post.models import Post


class CreateCommentSerializers(ModelSerializer):
    class Meta:
        model=Comment
        exclude=["created",]

    def validate(self, attrs):
        if attrs["parent"]:
            if attrs["parent"].post != attrs["post"]:
                raise serializers.ValidationError("yanlış giden şeyler")
        return attrs

class UserSerializer(ModelSerializer):
    class Meta:
        model= User
        fields=["first_name","email","is_superuser","id"]

class PostSerializer(ModelSerializer):
    class Meta:
        model= Post
        fields=["title","slug","id"]

class CommentListSerializer(ModelSerializer):
    replies=SerializerMethodField()
    user=UserSerializer()
    post=PostSerializer()
    class Meta:
        model=Comment
        fields="__all__"

    def get_replies(self,obj):
        if obj.any_children:
            return CommentListSerializer(obj.children(),many=True).data

class CommenUpdateDeleteSerializer(ModelSerializer):
    class Meta:
        model=Comment
        fields=["content"]
