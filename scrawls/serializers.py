from rest_framework import serializers
from .models import Wall, Comment


class WallSerializer(serializers.ModelSerializer):
    comments = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Wall
        fields = ("name", "lat", "lng", "comments")

class WallsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wall
        fields = ("name", "lat", "lng")

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("comment",)
