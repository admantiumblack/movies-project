from django.contrib import admin
from django.urls import path
from movies.views import movie_list, movie_view

app_name = "movies"
urlpatterns = [
    path("", movie_list, name="list"),
    path("detail", movie_view, name="detail")
]
