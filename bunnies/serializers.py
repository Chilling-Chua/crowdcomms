import http

from django.http import HttpResponseBadRequest
from rest_framework import serializers

from bunnies.models import Bunny, RabbitHole


class RabbitHoleSerializer(serializers.ModelSerializer):

    bunnies = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Bunny.objects.all()
    )
    bunny_count = serializers.SerializerMethodField()

    def get_bunny_count(self, obj) -> int:
        return Bunny.objects.filter(home__location=obj.location).count()

    def validate(self, attrs):
        attrs["owner"] = self.context["request"].user
        return attrs

    class Meta:
        model = RabbitHole
        fields = ("location", "bunnies", "bunny_count", "owner")


class BunnySerializer(serializers.ModelSerializer):

    home = serializers.SlugRelatedField(
        queryset=RabbitHole.objects.all(), slug_field="location"
    )
    family_members = serializers.SerializerMethodField()

    def get_family_members(self, obj):
        return [bunnie.name for bunnie in obj.home.bunnies.exclude(name=obj.name).all()]

    def validate(self, attrs):
        home = attrs["home"]
        if home.bunnies.count() >= home.bunnies_limit:
            raise serializers.ValidationError("Too many bunnies ... yes, that's possible ;) ")
        return attrs

    class Meta:
        model = Bunny
        fields = ("name", "home", "family_members")
