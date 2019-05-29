from django.urls import path

from . import views

app_name = 'scrawls'
urlpatterns = [
    path('walls', views.CreateWall.as_view(), name='walls-create'),
    path('walls/nearest', views.WallIndex.as_view(), name='walls-nearest'),
    path('walls/<int:pk>', views.WallShow.as_view(), name='wall-show'),
    path('walls/<int:pk>/comments', views.CreateComment.as_view(), name='comments-create'),
]
