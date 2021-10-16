from django.db.models import query
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets, mixins, serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

import random

from .models import Receipe, WhySlowcooker
from .serializers import (
    ReceipeSerializer,
    ReceipeGallerySerializer,
    WhySlowcookerSerializer,
)


def home(request):
    """Django view Home"""

    content = {}
    return render(request, "api/home.html", content)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class ReceipesView(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    pagination_class = StandardResultsSetPagination
    serializer_class = ReceipeSerializer
    lookup_field = "receipe_id"

    def get_queryset(self):
        queryset = Receipe.objects.all()
        findit = self.request.query_params.get("search")
        if findit:
            queryset = queryset.filter(name__contains=findit)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        query_param = self.request.query_params.get("likes_counter")
        if query_param == "up":
            instance.likes += 1
        if query_param == "down":
            instance.likes -= 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class NoIdeaReceipesView(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ReceipeSerializer

    def get_queryset(self):
        query_num = self.request.query_params.get("num")
        try:
            query_num.isnumeric()
            get_num = int(query_num)
        except (AttributeError, ValueError):
            get_num = 3

        all_values = Receipe.objects.values_list("id", flat=True)
        rand_entities = random.sample(list(all_values), get_num)
        queryset = Receipe.objects.filter(id__in=rand_entities)
        return queryset


class WhySlowcookerView(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = WhySlowcookerSerializer
    queryset = WhySlowcooker.objects.all()


class GalleryView(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    serializer_class = ReceipeGallerySerializer

    def get_queryset(self):

        queryset = Receipe.objects.order_by("-id")[:9]
        findit = self.request.query_params.get("filter")
        if findit:
            queryset = queryset[:10]
        return queryset
