from django.urls import path

from . import views

app_name = "movies"

urlpatterns = [
    # path(<path>, function reference, path_name)
    # path("", views.index, name="movies_index"), # good practice to prefix app name
    # or better way, declare app_name and reference URLs in template using <app_name>:<view>
    path("", views.index, name="index"),
    # movies/1, movies will be chopped off
    path("<int:movie_id>", views.detail, name="detail"),
]
