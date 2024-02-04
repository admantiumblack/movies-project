from rest_framework import serializers

from movies import models


class GetMovieParam(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False)
    include = serializers.ListField(child=serializers.CharField(), required=False)

    def validate(self, data):
        if "id" in data and "name" in data:
            raise serializers.ValidationError(
                "id and name cannot be used at the same time"
            )
        return data


class DynamicModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        exclude = kwargs.pop("exclude", None)

        # Instantiate the superclass normally
        super(DynamicModelSerializer, self).__init__(*args, **kwargs)

        if exclude is not None:
            not_allowed = set(exclude)
            for exclude_name in not_allowed:
                self.fields.pop(exclude_name)


class MPAARatingSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.MPAARating


class MPAARatingMappingSerializer(serializers.ModelSerializer):
    rating = MPAARatingSerializer(read_only=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["type"] = ret.pop("rating", {}).get("ratingType", None)

        return ret

    class Meta:
        fields = (
            "label",
            "rating",
        )
        model = models.MPARatingMapping


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.Genre


class MovieSerializer(DynamicModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    # uses many to handle RelatedManager Object
    mpaaRating = MPAARatingMappingSerializer(read_only=True, many=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if "genre" in ret:
            ret["genre"] = [i["genreName"] for i in ret["genre"]]
        if "mpaaRating" in ret:
            ret["mpaaRating"] = ret["mpaaRating"][0]

        return ret

    class Meta:
        fields = "__all__"
        model = models.Movie
