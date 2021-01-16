from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

    def is_password_length_valid(self):
        """
        Returns true if password is at least eight character long
        """

        return len(self.password) >= 8

    def do_upper_in_password(self):
        """
        Returns true if password contains at least one uppercase else false
        """ 

        return any(c.isupper() for c in self.password)

    def do_lower_in_password(self):
        """
        Returns if true if password contains at least one lower case else false
        """

        return any(c.islower() for c in self.password)

    def do_digit_in_password(self):
        """
        Returns if true if password contains at least one digit else false
        """

        return any(c.isdigit() for c in self.password)

    def do_passwords_match(self, confirmation):
        """
        Returns true if passwords match else false
        """

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
    
