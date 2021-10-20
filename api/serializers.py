from rest_framework import serializers
from .models import recipe, WhySlowcooker


class recipeSerializer(serializers.ModelSerializer):
    images = serializers.StringRelatedField(many=True)

    class Meta:
        model = recipe
        fields = [
            "recipe_id",
            "name",
            "slug",
            "serving_size",
            "preparing_time",
            "time_on_high",
            "time_on_low",
            "recipe_ingredients",
            "recipe_how_to",
            "images",
            "views",
            "likes",
        ]


class recipeGallerySerializer(serializers.ModelSerializer):
    images = serializers.StringRelatedField(many=True)

    class Meta:
        model = recipe
        fields = ["recipe_id", "name", "slug", "images"]


class WhySlowcookerSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhySlowcooker
        fields = ["heading", "paragraph", "icon"]
