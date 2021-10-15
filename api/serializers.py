from rest_framework import serializers
from .models import Receipe, WhySlowcooker


class ReceipeSerializer(serializers.ModelSerializer):
    images = serializers.StringRelatedField(many=True)
    class Meta:
        model = Receipe
        fields = ['receipe_id', 'name', 'slug',
            'serving_size', 'preparing_time',
            'time_on_high', 'time_on_low',
            'receipe_ingredients', 'receipe_how_to',
            'images']


class ReceipeGallerySerializer(serializers.ModelSerializer):
    images = serializers.StringRelatedField(many=True)
    class Meta:
        model = Receipe
        fields = ['receipe_id', 'name', 'slug', 'images']


class WhySlowcookerSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhySlowcooker
        fields = ['heading', 'paragraph', 'icon']