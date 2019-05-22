from rest_framework import serializers
from .models import Wall


class WallsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wall
        fields = ("name", "address", "lat", "lng", "range")
