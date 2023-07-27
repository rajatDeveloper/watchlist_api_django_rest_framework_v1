from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class RegistrationTestCase(APITestCase):
    def test_registration(self):
        data = {
            "username": "testcase",
            "email": "rk@example.com",
            "password": "abcd@1234",
            "password2": "abcd@1234"
            }
        
        response = self.client.post(reverse('register'), data)
        print("Response of register test case ->")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
class LoginLogoutTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="example", password="abcd@1234")
    
    def test_login(self):
        data = {
            "username": "example",
            "password": "abcd@1234"
            }
        
        response = self.client.post(reverse('login'), data)
        print("Response of login test case -> ")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)    
    
    def test_logout(self):
        # we need to pass token key in header as Authorization  = Token <token_key>
        self.token = Token.objects.get(user__username="example")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        response = self.client.post(reverse('logout'))
        print("Response of logout test case -> ")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
        
             
        
        
        
        
        



