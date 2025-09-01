from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="downloads-index"),
    path("<str:id>/", views.detail, name="downloads-detail"),
    path(
        "log/<str:work_dir>/<str:log_file>/", views.view_log, name="downloads-view-log"
    ),
    path("<str:work_dir>/delete/", views.delete_job, name="downloads-delete-job"),
]
