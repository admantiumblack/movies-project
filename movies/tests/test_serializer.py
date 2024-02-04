import pytest
from django_mock_queries.query import MockModel

from movies import serializer


class TestGetMovieParam:
    SERIALIZER = serializer.GetMovieParam

    @pytest.mark.parametrize(
        "input, expected_output",
        [
            ({"name": "test", "include": ["test1", "test2"]}, True),
            ({"id": 11}, True),
            ({"id": 12, "name": "test"}, False),
        ],
    )
    def test_validation(self, input, expected_output):
        param_serializer = self.SERIALIZER(data=input)

        assert param_serializer.is_valid() == expected_output


class TestMovieSerializer:
    SERIALIZER = serializer.MovieSerializer

    @pytest.mark.parametrize(
        "input, expected_output",
        [
            (
                MockModel(
                    id=1,
                    name="name1",
                    description="",
                    imgPath="path",
                    duration=100,
                    language="english",
                    userRating=4,
                    genre=[
                        MockModel(id=1, genreName="t"),
                        MockModel(id=2, genreName="e"),
                    ],
                    mpaaRating=[
                        MockModel(rating=MockModel(id=1, ratingType="pg"), label="test")
                    ],
                ),
                {
                    "id": 1,
                    "name": "name1",
                    "description": "",
                    "imgPath": "path",
                    "duration": 100,
                    "language": "english",
                    "userRating": 4,
                    "genre": ["t", "e"],
                    "mpaaRating": {"label": "test", "type": "pg"},
                },
            ),
        ],
    )
    def test_validation(self, input, expected_output):
        param_serializer = self.SERIALIZER(input)

        assert param_serializer.data == expected_output
    
    @pytest.mark.parametrize(
        "exclude, input, expected_output",
        [
            (
                ["genre"],
                MockModel(
                    id=1,
                    name="name1",
                    description="",
                    imgPath="path",
                    duration=100,
                    language="english",
                    userRating=4,
                    genre=[
                        MockModel(id=1, genreName="t"),
                        MockModel(id=2, genreName="e"),
                    ],
                    mpaaRating=[
                        MockModel(rating=MockModel(id=1, ratingType="pg"), label="test")
                    ],
                ),
                {
                    "id": 1,
                    "name": "name1",
                    "description": "",
                    "imgPath": "path",
                    "duration": 100,
                    "language": "english",
                    "userRating": 4,
                    "mpaaRating": {"label": "test", "type": "pg"},
                },
            ),
            (
                ["mpaaRating"],
                MockModel(
                    id=1,
                    name="name1",
                    description="",
                    imgPath="path",
                    duration=100,
                    language="english",
                    userRating=4,
                    genre=[
                        MockModel(id=1, genreName="t"),
                        MockModel(id=2, genreName="e"),
                    ],
                    mpaaRating=[
                        MockModel(rating=MockModel(id=1, ratingType="pg"), label="test")
                    ],
                ),
                {
                    "id": 1,
                    "name": "name1",
                    "description": "",
                    "imgPath": "path",
                    "duration": 100,
                    "language": "english",
                    "userRating": 4,
                    "genre": ["t", "e"],
                },
            ),
        ],
    )
    def test_exclusion(self, exclude, input, expected_output):
        param_serializer = self.SERIALIZER(input, exclude=exclude)

        assert param_serializer.data == expected_output
