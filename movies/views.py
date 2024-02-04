from django.http import JsonResponse
from rest_framework import status
from django.template.response import TemplateResponse
from rest_framework.decorators import api_view
from django.views.decorators.http import require_GET

from movies import serializer
from movies.models import Movie
from movies.repository import MovieRepository


# Create your views here.
@api_view(["GET"])
def movie_list(request):
    param = request.GET
    param_serializer = serializer.GetMovieParam(data=param)
    if not param_serializer.is_valid():
        response = {
            "meta": {
                "status": status.HTTP_400_BAD_REQUEST,
            },
            "data": param_serializer.errors,
        }
        return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST)

    validated_query = param_serializer.validated_data
    queryset = Movie.objects.get_queryset()
    if "id" in validated_query:
        queryset = MovieRepository.search_by_id(queryset, validated_query["id"])
    elif "name" in validated_query:
        queryset = MovieRepository.search_by_name(queryset, validated_query["name"])
        print(queryset.all())

    excluded_fields = {"genre", "mpaaRating"}
    if "include" in validated_query:
        included = validated_query["include"]
        if "genre" in included:
            queryset = queryset.prefetch_related("genre")
            excluded_fields.remove("genre")
        if "rating" in included:
            excluded_fields.remove("mpaaRating")

    data = queryset.all()
    data = serializer.MovieSerializer(data, many=True, exclude=excluded_fields).data
    response = {
        "meta": {"count": len(data), "status": status.HTTP_200_OK},
        "data": data,
    }
    print(response)
    return JsonResponse(response, status=status.HTTP_200_OK)


@require_GET
def movie_view(request):
    param = request.GET
    param_serializer = serializer.GetMovieParam(data=param)
    if not param_serializer.is_valid():
        response = {
            "meta": {
                "status": status.HTTP_400_BAD_REQUEST,
            },
            "data": param_serializer.errors,
        }
        return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST)
    validated_query = param_serializer.validated_data

    queryset = Movie.objects.get_queryset()
    queryset = MovieRepository.search_by_id(queryset, validated_query["id"])
    data = queryset.first()
    data = serializer.MovieSerializer(data).data
    context = {
        "title": data["name"],
        "mpaaRating": data["mpaaRating"]["type"],
        "label": data["mpaaRating"]["label"],
        "imgPath": data["imgPath"],
        "language": data["language"],
        "duration": data["duration"],
        "userRating": data["userRating"],
        "description": data["description"],
        "genres": ",".join(data["genre"]),
    }
    return TemplateResponse(request, "moviepage.html", context=context)
