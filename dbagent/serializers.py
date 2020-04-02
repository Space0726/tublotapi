from rest_framework import serializers

from . import models

class VideoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Video
        fields = [
            'id',
            'title',
            'description',
            'category',
            'view_count',
            'like_count',
            'dislike_count',
            'favorite_count',
            'comment_count',
            'comment_sentiment',
            'published_at',
            'duration',
        ]
