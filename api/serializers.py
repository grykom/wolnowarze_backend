from rest_framework import serializers
from .models import Recipe, WhySlowcooker


class RecipeSerializer(serializers.ModelSerializer):
    images = serializers.StringRelatedField(many=True)

    class Meta:
        model = Recipe
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


class RecipeGallerySerializer(serializers.ModelSerializer):
    images = serializers.StringRelatedField(many=True)

    class Meta:
        model = Recipe
        fields = ["recipe_id", "name", "slug", "images"]


class WhySlowcookerSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhySlowcooker
        fields = ["heading", "paragraph", "icon"]
