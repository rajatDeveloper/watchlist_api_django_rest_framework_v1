
from rest_framework.decorators import api_view
from user_app.api.serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from user_app  import models
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@api_view(['POST'])
def  regisgration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {};
        if serializer.is_valid():
            
            account = serializer.save()
            #normal token
            token = Token.objects.get(user=account).key
            print(token)
            data['token']  = token
            return Response(data , status=status.HTTP_201_CREATED) 
            #--?> jwt token 
            # data= get_tokens_for_user(account)
            # return Response(data , status=status.HTTP_201_CREATED)
            
        else : 
            data = serializer.errors
            return Response(data , status=status.HTTP_400_BAD_REQUEST) 
         
        
@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response( {
            "message" : "logout successfully"
            }, status=status.HTTP_200_OK)    
            
     