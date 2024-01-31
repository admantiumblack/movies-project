from django.core.management.base import BaseCommand, CommandParser
from movies import models
import json
from operator import itemgetter


class Command(BaseCommand):
    help = """
    seed database
    """

    def add_arguments(self, parser: CommandParser) -> None:
        super().add_arguments(parser)
        parser.add_argument("--file", type=str, default="seed.json")

    def _create_genre(self, genre_list):
        genres = []
        for i in genre_list:
            genres.append(models.Genre.objects.get_or_create(genreName=i)[0])
        return genres

    def get_or_create_rating(self, rating_type):
        rating = models.MPAARating.objects.filter(ratingType=rating_type).first()
        if rating is None:
            rating = models.MPAARating.objects.create(ratingType=rating_type)
        return rating

    def _seed(self, data):
        movie_field = [
            "id",
            "name",
            "description",
            "duration",
            "imgPath",
            "duration",
            "language",
            "userRating",
        ]

        for i in data:
            movie_data = {x: i[x] for x in movie_field}
            movie = models.Movie.objects.create(**movie_data)

            genre_list = i["genre"]
            genres = self._create_genre(genre_list)
            movie.genre.add(*genres)

            rating = i["mpaaRating"]
            mpaa_rating = self.get_or_create_rating(rating["type"])
            models.MPARatingMapping.objects.create(
                rating=mpaa_rating, movie=movie, label=rating["label"]
            )

    def _handle_file(self, file_path):
        with open(file_path, "r") as f:
            res = json.load(f)
        return res

    def handle(self, *args, **kwargs):
        data = self._handle_file(kwargs["file"])
        self._seed(data)
