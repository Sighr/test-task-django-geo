from rest_framework import serializers
from rest_framework_gis.serializers import GeometryField


class LineSerializer(serializers.Serializer):
    type = serializers.CharField(default="Feature")
    geometry = GeometryField()


class LineLengthSerializer(LineSerializer):
    class LengthSerializer(serializers.Serializer):
        length = serializers.FloatField()

    properties = LengthSerializer()


class LineScoreSerializer(LineSerializer):
    class ScoreSerializer(serializers.Serializer):
        score = serializers.IntegerField()

    properties = ScoreSerializer()
