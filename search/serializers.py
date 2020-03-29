from rest_framework import serializers
from .models import Search

class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'search_type',
            'search_word'
        )
        model = Search
