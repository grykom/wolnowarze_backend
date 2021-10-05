from rest_framework import serializers
from .models import Receipe, WhySlowcooker


class ReceipeSerializer(serializers.ModelSerializer):
    images = serializers.StringRelatedField(many=True)
    class Meta:
        model = Receipe
        fields = ['name', 'serving_size', 'preparing_time', 'time_on_high', 'images']


class ReceipeGallerySerializer(serializers.ModelSerializer):
    images = serializers.StringRelatedField(many=True)
    class Meta:
        model = Receipe
        fields = ['id', 'name', 'images']


class WhySlowcookerSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhySlowcooker
        fields = ['heading', 'paragraph', 'icon']