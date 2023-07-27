# from django.shortcuts import render
# from watchlist_app.models import Movie 
# from django.http import JsonResponse


# # Create your views here.
# def movie_list(request):
#     movies = Movie.objects.all()
    
#     return JsonResponse({'movies':list(movies.values())})


# def movie_item(required  , pk ):
#     try:
#         movie = Movie.objects.get(pk=pk) 
#         data = {
#             'name':movie.name,
#             'description':movie.description,
#             'active':movie.active
#         }
#         return JsonResponse(data)
#     except Movie.DoesNotExist:
#         return JsonResponse({'error':'Movie not found'}, status=404)
    
    