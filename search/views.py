from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics

from .models import Search
from .serializers import SearchSerializer

class ListSearch(generics.ListCreateAPIView):
    queryset = Search.objects.all()
    serializer_class = SearchSerializer

def search(request):
    print(request.body)
    return HttpResponse(request.body)

