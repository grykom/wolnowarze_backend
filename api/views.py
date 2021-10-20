from django.shortcuts import render
from rest_framework import status, viewsets, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

import random

from .models import recipe, WhySlowcooker
from .serializers import (
    recipeSerializer,
    recipeGallerySerializer,
    WhySlowcookerSerializer,
)


def home(request):
    content = {}
    return render(request, "api/home.html", content)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class recipesView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    pagination_class = StandardResultsSetPagination
    serializer_class = recipeSerializer
    lookup_field = "recipe_id"

    def get_queryset(self):
        queryset = recipe.objects.all()
        findit = self.request.query_params.get("search")
        if findit:
            queryset = queryset.filter(name__contains=findit)
        return queryset

    def retrieve(self, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def likes(self, *args, **kwargs):
        up_down_action = kwargs['up_down']
        if up_down_action in ['up', 'down']:
            instance = self.get_object()
            if up_down_action == 'up':
                instance.likes += 1
            else:
                instance.likes -= 1
            instance.save()
            return Response({ 'likes': instance.likes })
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class NoIdearecipesView(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
    ):
    serializer_class = recipeSerializer

    def get_queryset(self):
        query_num = self.request.query_params.get("num")
        try:
            query_num.isnumeric()
            get_num = int(query_num)
        except (AttributeError, ValueError):
            get_num = 1

        all_values = recipe.objects.values_list("id", flat=True)
        rand_entities = random.sample(list(all_values), get_num)
        queryset = recipe.objects.filter(id__in=rand_entities)
        return queryset


class WhySlowcookerView(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = WhySlowcookerSerializer
    queryset = WhySlowcooker.objects.all()


class GalleryView(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = recipeGallerySerializer

    def get_queryset(self):
        query_num = self.request.query_params.get("num")
        try:
            query_num.isnumeric()
            get_num = int(query_num)
        except (AttributeError, ValueError):
            get_num = 1

        all_values = recipe.objects.values_list("id", flat=True)
        rand_entities = random.sample(list(all_values), get_num)
        queryset = recipe.objects.filter(id__in=rand_entities)
        return queryset
