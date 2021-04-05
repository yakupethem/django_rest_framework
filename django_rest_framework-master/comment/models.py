from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from post.models import Post


class Comment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,related_name="post", on_delete=models.CASCADE)
    content=models.TextField()
    parent=models.ForeignKey("self",related_name="replies",null=True,blank=True,on_delete=models.CASCADE)
    created=models.DateTimeField(editable=False)

    class Meta:
        ordering=("created",)

    def __str__(self):
        return self.post.title+" - "+self.user.username

    def save(self,*args,**kwargs):
        if not self.id:
            self.created=timezone.now()
        self.modified=timezone.now()
        return super(Comment,self).save(*args,**kwargs)

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def any_children(self):
        return Comment.objects.filter(parent=self).exists()
