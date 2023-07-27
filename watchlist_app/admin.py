from django.contrib import admin
from watchlist_app.models import WatchList , StreamPlatform  , Review
# Register your models here.


admin.site.register(WatchList, list_display=['id' , 'title' , 'storyline' , 'active' , 'created' , 'platform'])

admin.site.register(StreamPlatform, list_display=['id' , 'name' , 'about' , 'website'])

admin.site.register(Review, list_display=['id' , 'rating' , 'description' , 'active' , 'created' , 'updated' , 'watchlist' , 'review_user'])


 