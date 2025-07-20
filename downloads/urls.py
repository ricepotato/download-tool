from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("log/<str:work_dir>/<str:log_file>/", views.view_log, name="view_log"),
    path("delete/<str:work_dir>/", views.delete_job, name="delete_job"),
    # path("stream/<str:m3u8_file_name>/", views.stream_mp4, name="stream_mp4"),
]
