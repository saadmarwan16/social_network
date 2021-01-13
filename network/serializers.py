from .models import User, Post, Follow, Like
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'content', 'timestamp', 'num_of_likes', 'num_of_comments', 'poster')


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'is_liked')