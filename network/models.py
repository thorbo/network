from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField("self", blank=True, null=True, related_name="followers", symmetrical=False)
    liked = models.ManyToManyField("Posts", blank=True, null=True, related_name="likers", symmetrical=False)
    pass

# class Follow(models.Model):
#     follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followings")
#     following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")


class Posts(models.Model):
    content = models.CharField(max_length=128)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    likes = models.IntegerField()
    postTime = models.DateTimeField()

    def serialize(self):
        return {
            "content": self.content,
            "poster": self.poster.username,
            "likes": self.likes,
            "postTime": self.postTime.strftime("%b %d %Y, %I:%M %p")
        }
