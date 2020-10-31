"""
Ключевые слова: views, serializer

POST запросы:
    - На создание SiteEvent
    - На создание Site
    - На создание Worker
"""
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from .serializers import *
from server.models import *


class SiteEventCreateView(generics.CreateAPIView):
    serializer_class = SiteEventSerializer

    def perform_create(self, serializer):
        return serializer.save()


class SiteCreateView(generics.CreateAPIView):
    serializer_class = SiteSerializer

    def perform_create(self, serializer):
        return serializer.save()
