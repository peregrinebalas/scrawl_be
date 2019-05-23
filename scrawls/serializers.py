from rest_framework import serializers
from .models import Wall, Comment


class WallsSerializer(serializers.ModelSerializer):
    comments = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Wall
        fields = ("name", "address", "lat", "lng", "range", "comments")

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("comment")



# class WallCommentsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Wall
