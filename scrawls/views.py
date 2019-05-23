from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import status

from .serializers import WallsSerializer
from .models import Wall, Comment


class CreateWall(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        name = request.data.get("name", "")
        address = request.data.get("address", "")
        lat = request.data.get("lat", "")
        lng = request.data.get("lng", "")
        range = request.data.get("range", "")
        if not name and not address and not lat and not lng and not range:
            return Response(data={
                "error": "Could not save Wall."
            }, status=status.HTTP_409_CONFLICT)
        wall = Wall.objects.get_or_create(
            name=name,
            address=address,
            lat=lat,
            lng=lng,
            range=range
        )
        msg = "%s can be found at %s." % (name, address)
        return Response(data={
            "message": msg
        }, status=status.HTTP_201_CREATED)


class WallShow(generics.RetrieveAPIView):

    def get(self, request, **kwargs):
        wall = Wall.objects.get(pk=kwargs['pk'])
        return Response(data = WallsSerializer(wall).data, status=status.HTTP_200_OK)
