from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from watchlist_app.models import WatchList   , StreamPlatform , Review
from watchlist_app.api.serializers import WatchListSerializer , StreamPlatformSerializer , ReviewSerializer
# from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView

from rest_framework import mixins
from rest_framework import generics

from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
# class StreamPlatformVS(viewsets.ReadOnlyModelViewSet):
#     queryset = StreamPlatform.objects.all()
#     serializer_class = StreamPlatformSerializer 
from watchlist_app.api.permissions import IsAdminOrReadOnly , IsReviewUserOrReadOnly  

from rest_framework.permissions import IsAuthenticatedOrReadOnly , IsAuthenticated


from django_filters.rest_framework import DjangoFilterBackend 
from rest_framework import filters

from watchlist_app.api.pagination import WatchListPagination , WatchListLOPagination , WatchListCPagination

class StreamPlatformVS(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer 


# class StreamPlatformVS(viewsets.ViewSet):
#     def list (self  , request):
#         platform = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(platform, many=True)
#         return Response(serializer.data)
    
#     def retrieve(self , request , pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)
    
#     def create(self , request):
#         serializer = StreamPlatformSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else : 
#             return Response(serializer.errors)
        
    
    
    

class StreamPlatformDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self , request , pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
            serializer = StreamPlatformSerializer(platform )
            return Response(serializer.data)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'StreamPlatform not found'}, status=404)
    
    def put(self , request , pk):
        platform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(platform , data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else :
            return Response(serializer.errors) 
        
    def delete(self , request , pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
            platform.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'error': 'StreamPlatform not found'}, status=404)
        

class StreamPlatformAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get (self , request):
        platform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platform , many=True 
                                            #   ,context={'request': request}
                                              )
        return Response(serializer.data)
    
    def post(self , request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else :
            return Response(serializer.errors)


# api view class 
class WatchListAV(APIView):
    # permission_classes = [IsAuthenticatedOrReadOnly]
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self , request):
        movies = WatchList .objects.all()
        serializer = WatchListSerializer(movies, many=True) 
        return Response(serializer.data)
    
    def post(self , request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else :
            return Response(serializer.errors)
        

class WatchDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self,request, pk ):
        try: 
            movie = WatchList .objects.get(pk=pk)
            return Response(WatchListSerializer(movie).data)
        except WatchList.DoesNotExist:
            return Response({'error': 'WatchList  not found'}, status=404) 
        
    def put(self  ,  request , pk):
        
        if serializer.is_valid():
            movie = WatchList.objects.get(pk=pk)
            serializer = WatchListSerializer(movie, data=request.data)
            serializer.save()
            return Response(serializer.data)
        else :
            return Response(serializer.errors)   
        
    def delete(self   , request   , pk):
        try:
            movie = WatchList .objects.get(pk=pk)
            movie.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)    
        except WatchList .DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)     
     
     
     
class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist = pk )
       
    
    
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsReviewUserOrReadOnly]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer    
    
class ReviewCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        watchlist = WatchList.objects.get(pk=pk)
        
        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist , review_user=review_user)
        
        if review_queryset.exists() :
            raise ValidationError({'error': 'You have already reviewed this movie'})
        
        
        if watchlist.number_rating == 0 :
            watchlist.avg_rating = serializer.validated_data['rating'] 
        else: 
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2         
        
        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()
        
        serializer.save(watchlist=watchlist , review_user=review_user)
        

class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    #flitering from url 
    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return Review.objects.filter(review_user__username = username)
    # filtering using qy=uery 
    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        
        return Review.objects.filter(review_user__username = username)
    
     

class WatchListGV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    
    pagination_class = WatchListCPagination
    
    filter_backends = [DjangoFilterBackend , filters.SearchFilter , 
                    #    filters.OrderingFilter
                       ]
    filterset_fields = ['title', 'platform__name']
    search_fields = ['title'  , 'platform__name']
    # ordering_fields = ['-avg_rating']
    
    
    
    
       
# class ReviewList(mixins.ListModelMixin, 
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# class ReviewDetail(mixins.RetrieveModelMixin  , mixins.UpdateModelMixin , mixins.DestroyModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
    
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
    
#     def delete(self, request, *args, **kwargs):
#         return self.delete(request, *args, **kwargs)
    
    
# class ReviewListAV(APIView):
#     def get(self , request ):
#         reviews = Review.objects.all()
#         serializer = ReviewSerializer(reviews , many=True)
#         return Response(serializer.data)  
    
#     def post(self , request , pk):
#         serializer = ReviewSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else :
#             return Response(serializer.errors)   
        
        
        
# class ReviewDetailAV(APIView):
#     def get(self , request , pk):
#         try:
#             review = Review.objects.get(pk=pk)
#             serializer = ReviewSerializer(review)
#             return Response(serializer.data)
#         except Review.DoesNotExist:
#             return Response({'error': 'Review not found'}, status=404) 
        
#     def put(self , request , pk):
#         review = Review.objects.get(pk=pk)
#         serializer = ReviewSerializer(review , data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else :
#             return Response(serializer.errors) 
        
#     def delete(self , request , pk):
#         try:
#             review = Review.objects.get(pk=pk)
#             review.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except:
#             return Response({'error': 'Review not found'}, status=404)

    

# # api view class 
# class MovieListAV(APIView):
    
#     def get(self , request):
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True) 
#         return Response(serializer.data)
    
#     def post(self , request):
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else :
#             return Response(serializer.errors)
        

# class MovieDetailAV(APIView):
#     def get(self ,  request       , pk ):
#         try: 
#             movie = Movie.objects.get(pk=pk)
#             return Response(MovieSerializer(movie).data)
#         except Movie.DoesNotExist:
#             return Response({'error': 'Movie not found'}, status=404) 
        
#     def put(self  ,  request , pk):
        
#         if serializer.is_valid():
#             movie = Movie.objects.get(pk=pk)
#             serializer = MovieSerializer(movie, data=request.data)
#             serializer.save()
#             return Response(serializer.data)
#         else :
#             return Response(serializer.errors)   
        
#     def delete(self   , request   , pk):
#         try:
#             movie = Movie.objects.get(pk=pk)
#             movie.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)    
#         except Movie.DoesNotExist:
#             return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)     
           
            
        
    
    



# dectortor api view   - view 

# @api_view(['GET' , 'POST' ])
# def movie_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerialozer(movies, many=True) 
#         return Response(serializer.data)
#     if request.method == 'POST':
#         serializer = MovieSerialozer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else :
#             return Response(serializer.errors)
 
 
# @api_view(['GET' , 'PUT' , 'DELETE'])   
# def movie_item(request  , pk):
#     if request.method == 'GET':
#         try:
#             movie = Movie.objects.get(pk=pk)
#             data = MovieSerialozer(movie)
#             return Response(data.data)
#         except Movie.DoesNotExist:
#             return Response({'error': 'Movie not found'}, status=404)
        
#     if request.method == 'PUT':
#         movie = Movie.objects.get(pk=pk)
#         serializer = MovieSerialozer(movie , data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else :
#             return Response(serializer.errors)   
        
#     if request.method == 'DELETE':
#         try:
#             movie = Movie.objects.get(pk=pk)
#             movie.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)    
#         except Movie.DoesNotExist:
#             return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND) 


