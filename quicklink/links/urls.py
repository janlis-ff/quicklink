from django.urls import path

from quicklink.links import views

app_name = "links"

urlpatterns = [
    path(
        "",
        views.LinkCreateView.as_view(),
        name="link-create",
    ),
]
