from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # path("stream/<str:m3u8_file_name>/", views.stream_mp4, name="stream_mp4"),
]
