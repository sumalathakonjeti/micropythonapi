from django.db import models

# Create your models here.

class Book(models.Model):
    name = models.CharField(max_length=256)
    author = models.CharField(max_length=128)
    rating = models.FloatField
    reviews = models.IntegerField
    price = models.IntegerField
    year = models.CharField(max_length=8)
    genre = models.CharField(max_length=32)
    
    def __str__(self):
        return self.name