from django.contrib import admin
from django.urls import path
from movies.views import movie_list

urlpatterns = [
    path("", movie_list),
]
