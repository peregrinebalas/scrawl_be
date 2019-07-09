from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('api/v1/', include('scrawls.urls')),
    path('admin/', admin.site.urls)
]
