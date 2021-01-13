from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

    def is_password_valid(self):
        """
        Returns true password has at least one uppercase, at least one lower case, at least one digit and
        is at least eight character long
        """

        return (any(c.isupper() for c in self.password) and any(c.islower() for c in self.password)
            and any(c.isdigit() for c in self.password) and len(self.password) >= 8)

    def do_passwords_match(self, confirmation):
        return self.password == confirmation


class Post(models.Model):
    content = models.CharField(max_length=2560)
    timestamp = models.DateTimeField(auto_now_add=True)
    num_of_likes = models.PositiveIntegerField(default=0)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    def __str__(self):
        return f"{self.content}"

    def increase_likes(self):
        self.num_of_likes += 1
        self.save()

    def decrease_likes(self):
        self.num_of_likes -= 1
        self.save()


class Like(models.Model):
    is_liked = models.BooleanField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="number_of_likes")
    user = models.ManyToManyField(User, related_name="liked")

    def __str__(self):
        if self.is_liked:
            return f"{self.user} liked {self.post}"

        else:
            return f"{self.user} didn't like {self.post}"


class Follow(models.Model):
    is_following = models.BooleanField()
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")

    def __str__(self):
        return f"{self.follower} follows {self.followee}"
    
