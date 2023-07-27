from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from watchlist_app  import models 
from watchlist_app.api  import serializers


class StreamPlatformTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="example", password="abcd@1234")
        self.token = Token.objects.get(user__username="example")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.stream = models.StreamPlatform.objects.create(
            name="Amazon Prime",
            about="Prime videos" ,
            website="https://www.primevideo.com/")
    
    def test_streamplatform_create(self):
        
        data = {
            "name": "Amazon Prime",
            "about": "Prime videos" , 
            "website": "https://www.primevideo.com/"
        }
        response = self.client.post(reverse('streamplatform-list'), data)
        print("Response of streamplatform create test case -> ")
        print(response.data)
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_streamplatform_list(self):
        response = self.client.get(reverse('streamplatform-list'))
        print("Response of streamplatform list test case -> ")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)   
        
    def test_streamplatfrom_indivisual(self):
        response = self.client.get(reverse('streamplatform-detail', args=(self.stream.id,)))
        print("Response of streamplatform indivisual test case -> ")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        
        
class WatchListTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="example", password="abcd@1234")
        self.token = Token.objects.get(user__username="example")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.stream = models.StreamPlatform.objects.create(
            name="Amazon Prime",
            about="Prime videos" ,
            website="https://www.primevideo.com/")
        
        self.watchlist = models.WatchList.objects.create(
            platform = self.stream,
            title= "test movie",
            storyline= "test",
            active= True
        )
        
    
    def test_watchlist_create(self):
        data = {
            "platform": self.stream,
            "title": "test movie",
            "storyline": "test",
            "active": True
        }
        response = self.client.post(reverse('movie-list'), data)
        print("Response of watchlist create test case -> ")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_watchlist_list(self):
        response = self.client.get(reverse('movie-list'))
        print("Response of watchlist list test case -> ")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  
        
        
    def test_watchlist_indivisual(self):
        response = self.client.get(reverse('movie-item', args=(self.watchlist.id,)))
        print("Response of watchlist indivisual test case -> ")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  
        
class ReviewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="example", password="abcd@1234")
        self.token = Token.objects.get(user__username="example")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.stream = models.StreamPlatform.objects.create(
            name="Amazon Prime",
            about="Prime videos" ,
            website="https://www.primevideo.com/")
        
        self.watchlist = models.WatchList.objects.create(
            platform = self.stream,
            title= "test movie",
            storyline= "test",
            active= True
        )
        
        self.watchlist2 = models.WatchList.objects.create(
            platform = self.stream,
            title= "test movie22",
            storyline= "test 2",
            active= True
        )
        
        self.review = models.Review.objects.create(
            review_user = self.user,
            watchlist = self.watchlist2,
            rating = 5,
            description = "good movie"
        )
        
       
        
    def test_review_create(self):
        data = {
            "watchlist": self.watchlist,
            "rating": 5,
            "description": "good movie",
            "active": True
        }
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
       
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_review_create_unauth(self):
        data = {
            "review_name": self.user,
            "watchlist": self.watchlist,
            "rating": 5,
            "description": "good movie",
            "active": True
        }
        
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
           
        
    def test_review_update(self):
        
        data = {
            "watchlist": self.watchlist2,
            "rating": 4,
            "description": "good movie",
            "active": True
        }
        
        response = self.client.put(reverse('review-iteam', args=(self.review.id,)), data)
        print("Response of review update test case -> ")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_review_list(self):
        response = self.client.get(reverse('review-list', args=(self.watchlist2.id,)))
        print("Response of review list test case -> ")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_review_indivisual(self):
        response = self.client.get(reverse('review-iteam', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_review_user(self):
        response = self.client.get('/watch/reviews/?username='+self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
               
        
                 

