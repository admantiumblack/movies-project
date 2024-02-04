from movies.models import Movie


class MovieRepository:
    model = Movie

    @classmethod
    def search_by_name(cls, qs, name):
        return qs.filter(name__icontains=name)

    @classmethod
    def search_by_id(cls, qs, id):
        return qs.filter(id=id)
