from django.urls import path

from . import views

app_name = 'scrawls'
urlpatterns = [
    path('walls', views.CreateWall.as_view(), name='walls-create'),
    path('walls/<int:pk>', views.WallShow.as_view(), name='wall-show'),
]
