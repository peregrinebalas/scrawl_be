from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import status

from .serializers import WallsSerializer, CommentsSerializer
from .models import Wall, Comment


class CreateWall(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        name = request.data.get("name", "")
        lat = request.data.get("lat", "")
        lng = request.data.get("lng", "")
        try:
            wall = Wall.objects.create(
                name=name,
                lat=lat,
                lng=lng,
            )

            comment = wall.comment_set.create(
                comment = request.data.get("comment", "")
            )

            return Response(data= WallsSerializer(wall).data, status=status.HTTP_201_CREATED)
        except:
            return Response(data={
                "error": "Fields missing, could not save wall."
            }, status=status.HTTP_409_CONFLICT)


class WallShow(generics.RetrieveAPIView):

    def get(self, request, **kwargs):
        try:
            wall = Wall.objects.get(pk=kwargs['pk'])
            return Response(data= WallsSerializer(wall).data, status=status.HTTP_200_OK)
        except (KeyError, Wall.DoesNotExist):
            return Response(data= {"error": "Could Not Find Wall"}, status=status.HTTP_404_NOT_FOUND)

class CreateComment(generics.CreateAPIView):
    serializer_class = CommentsSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, **kwargs):
        comment = request.data.get("comment", "")
        try:
            wall = Wall.objects.get(pk=kwargs['pk'])
            Comment.objects.create(
                wall = wall,
                comment = comment
            )
            return Response(data={"message": "Comment Saved!"}, status=status.HTTP_201_CREATED)
        except (KeyError, Wall.DoesNotExist):
            return Response(data={"error": "Conflict!"}, status=status.HTTP_409_CONFLICT)
