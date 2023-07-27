from django.db import models
from django.core.validators import MinValueValidator , MaxValueValidator
# Create your models here.
from django.contrib.auth.models import User

class StreamPlatform(models.Model):
    name = models.CharField(max_length=30)
    about = models.CharField(max_length=100)
    website = models.URLField(max_length=100)
    
    def __str__(self):
        return self.name

class WatchList(models.Model):
    title = models.CharField(max_length=50)
    storyline = models.CharField(max_length=200)
    #related_name is used to access the watchlist from streamplatform
    platform = models.ForeignKey(StreamPlatform , on_delete=models.CASCADE , related_name="watchlist")
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    avg_rating = models.FloatField(default=0)
    number_rating = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title
    
class Review(models.Model):
    review_user = models.ForeignKey(User, on_delete=models.CASCADE )
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5) , MinValueValidator(1)])
    description = models.CharField(max_length=200 , null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    #related_name is used to access the reviews from watchlist
    watchlist = models.ForeignKey(WatchList , on_delete=models.CASCADE , related_name="reviews")
    
    def __str__(self):
        return str(self.rating) + " | " + self.watchlist.title






















# class Movie(models.Model):
#     name = models.CharField(max_length=100 ) 
#     description = models.TextField(max_length=1000)
#     active = models.BooleanField(default=True)
    
#     def __str__(self):
#         return self.name
    