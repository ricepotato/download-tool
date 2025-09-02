from django.urls import path

from . import views

urlpatterns = [
    path("", views.LinkListView.as_view(), name="link-index"),
    path("add-tags/<int:link_id>/", views.add_tags_to_link, name="add-tags"),
]
