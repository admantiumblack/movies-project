import pytest
from django_mock_queries.query import MockSet, MockModel

from movies import repository


class TestMovie:
    REPOSITORY = repository.MovieRepository

    @pytest.fixture
    def qs(self):
        movie_data = [
            {"name": "alpha", "id": 1},
            {"name": "beta", "id": 2},
            {"name": "alps", "id": 3},
            {"name": "marks", "id": 4},
        ]
        return MockSet(*[MockModel(i) for i in movie_data])

    @pytest.mark.parametrize(
        "input, expected_output", [("alp", [1, 3]), ("be", [2]), ("none", [])]
    )
    def test_search_by_name(self, qs, input, expected_output):
        res = self.REPOSITORY.search_by_name(qs.all(), input)
        # res = res.all()
        for model, id in zip(res, expected_output):
            assert model.id == id

    @pytest.mark.parametrize("input, expected_output", [(1, 1), (2, 2), (10, None)])
    def test_search_by_id(self, qs, input, expected_output):
        res = self.REPOSITORY.search_by_id(qs.all(), input)
        res = res.first()

        try:
            assert res.id == expected_output
        except AttributeError:
            assert expected_output is None and res is None
