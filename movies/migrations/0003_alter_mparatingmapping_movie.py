# Generated by Django 5.0 on 2024-02-04 05:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0002_rename_genre_name_genre_genrename_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mparatingmapping",
            name="movie",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="mpaaRating",
                to="movies.movie",
            ),
        ),
    ]
