from django.shortcuts import render
from rest_framework import viewsets

from . import models, serializers

class VideoViewSet(viewsets.ModelViewSet):
    queryset = models.Video.objects.all()
    serializer_class = serializers.VideoSerializer
