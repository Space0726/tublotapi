from django.db import models

class Video(models.Model):
    id = models.CharField(max_length=11, primary_key=True)
    title = models.TextField()
    description = models.TextField()
    channel = models.CharField(max_length=50)
    category = models.CharField(max_length=30)
    view_count = models.BigIntegerField()
    like_count = models.BigIntegerField()
    dislike_count = models.BigIntegerField()
    favorite_count = models.BigIntegerField()
    comment_count = models.BigIntegerField()
    comment_sentiment = models.FloatField()
    published_at = models.DateTimeField()
    duration = models.BigIntegerField()

    def __str__(self):
        return self.title
