from django.urls import path , include 
from watchlist_app.api.views import WatchDetailAV , WatchListAV , StreamPlatformAV , StreamPlatformDetailAV ,ReviewList   , ReviewDetail  , ReviewCreate , StreamPlatformVS , UserReview , WatchListGV
# ReviewListAV , ReviewDetailAV ,

# from watchlist_app.api.views import MovieDetailAV , MovieListAV
# from watchlist_app.api.views import movie_list  , movie_item
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('stream', StreamPlatformVS, basename='streamplatform')

urlpatterns = [
    path('list/', WatchListAV.as_view() , name='movie-list'),
    path('list-new/', WatchListGV.as_view() , name='movie-list-new'),
    path('<int:pk>/', WatchDetailAV.as_view() , name='movie-item'),
    path('' , include(router.urls)),
    # path('stream/', StreamPlatformAV.as_view() , name='stream-list'),
    # path('stream/<int:pk>', StreamPlatformDetailAV.as_view() , name='stream-iteam'),
    #create review direct using id in params or url pattern
    path('<int:pk>/review-create/', ReviewCreate.as_view() , name='review-create')  ,
    #give reivie for given id in params or url pattern
    path('<int:pk>/reviews/', ReviewList.as_view() , name='review-list')  , 
    path('review/<int:pk>/', ReviewDetail.as_view() , name='review-iteam') , 
    # path('review/', ReviewList.as_view() , name='review-list') , 
    # path('review/<int:pk>', ReviewDetail.as_view() , name='review-iteam') ,
    
    # path('review/', ReviewListAV.as_view() , name='review-list'),
    # path('review/<int:pk>', ReviewDetailAV.as_view() , name='review-iteam'),
    
    # path('list/', movie_list , name='movie-list'),
    # path('<int:pk>', movie_item , name='movie-ieam'),
    
    
    #filter from url
    # path('reviews/<str:username>/', UserReview.as_view() , name='user-review-detail')
    
     path('reviews/', UserReview.as_view() , name='user-review-detail')
]
