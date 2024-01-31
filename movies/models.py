from django.db import models


# Create your models here.
class Movie(models.Model):
    class RatingChoice(models.IntegerChoices):
        VERY_LOW = 1, "Very Low"
        LOW = 2, "Low"
        MODERATE = 3, "Moderate"
        HIGH = 4, "High"
        VERY_HIGH = 5, "Very High"

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    imgPath = models.CharField(max_length=100)
    duration = models.IntegerField()
    language = models.CharField(max_length=50)
    userRating = models.IntegerField(choices=RatingChoice.choices)
    genre = models.ManyToManyField("Genre")


class MPAARating(models.Model):
    id = models.AutoField(primary_key=True)
    ratingType = models.CharField(max_length=20)


class Genre(models.Model):
    id = models.AutoField(primary_key=True)
    genreName = models.CharField(max_length=50)


class MPARatingMapping(models.Model):
    rating = models.ForeignKey(
        "MPAARating", related_name="movies", on_delete=models.CASCADE
    )
    movie = models.ForeignKey(
        "Movie", related_name="mpaaRating", on_delete=models.CASCADE
    )
    label = models.CharField(max_length=255)

    class Meta:
        unique_together = ("rating", "movie")
