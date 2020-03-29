from django.db import models

class Search(models.Model):
    search_type = models.CharField(max_length=10)
    search_word = models.TextField()

    def __str__(self):
        return dict(search_type=search_type, search_word=search_word)
