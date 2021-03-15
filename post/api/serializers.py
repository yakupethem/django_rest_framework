from rest_framework import serializers
from post.models import Post


class PostSerialiers(serializers.ModelSerializer):

    url=serializers.HyperlinkedIdentityField(
        view_name="detail",
        lookup_field="slug"
    )


    username = serializers.SerializerMethodField()
    class Meta:
        model=Post
        fields=["url","username","title","content","created","slug","image","modified_by"]


    def get_username(self,obj):
        return str(obj.user.username)