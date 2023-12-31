from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth import authenticate,get_user_model
from rest_framework.authtoken.models import Token

User=get_user_model()


class RegisterView(APIView):
    def post(self,request):
        data=request.data
        serializer=RegisterSerializer(data=data)

        if not serializer.is_valid():
            return Response(
                {
                    'status':'False',
                    'message':serializer.errors
                }
            )
        serializer.save()
        return Response({'message':'User account created'})
    

class LoginView(APIView):

    def post(self , request):
        data = request.data
        serializer = LoginSerializer(data=data)

        if not serializer.is_valid():
            return Response({
                'status':False,
                'message':serializer.errors
            }) 

        user = authenticate(username = serializer.data['phoneNumber'] , password = serializer.data['password'])

        if not user:
            return Response({
                'status':False,
                'message': 'invalid credentials'
            })
        
        token = Token.objects.get_or_create(user=user)


        return Response({'message':"user login" , 'token':str(token)})
    
class UserListView(APIView):
    def get(self,request):
            users=User.objects.all()
            phone_number=[user.username for user in users]
            return Response({'phone_numbers': phone_number})