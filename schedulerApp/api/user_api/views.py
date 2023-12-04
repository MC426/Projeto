from django.contrib.auth import get_user_model, login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserLoginSerializer, UserSerializer
from rest_framework import permissions, status
from .validations import custom_validation, validate_email, validate_password
from .models import AppUser
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime


class UserRegister(APIView):
	permission_classes = (permissions.AllowAny,)
	def post(self, request):
		clean_data = custom_validation(request.data)
		serializer = UserSerializer(data=clean_data)
		if serializer.is_valid(raise_exception=True):
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = (SessionAuthentication,)
	##
	def post(self, request):
		data = request.data
		assert validate_email(data)
		assert validate_password(data)
		email = request.data['email']
		password = request.data['password']
		user = AppUser.objects.filter(email=email).first()

		if user is None:
			raise AuthenticationFailed('User not found')

		if not user.check_password(password):
			raise AuthenticationFailed('Incorrect Password')

		serializer = UserLoginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.check_user(data)
			login(request, user)
			payload = {
				'user_id': user.user_id,
				'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
				'iat': datetime.datetime.utcnow()
			}
		    
			token = jwt.encode(payload, 'secret', algorithm='HS256')

			response = Response()
			response.set_cookie(key='jwt', value=token, httponly=True)
			response.data = {
				'jwt': token
			}
			return response

class UserLogout(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = ()
	def post(self, request):
		logout(request)
		response = Response()
		response.delete_cookie('jwt')
		response.data = { 
			'message' : 'success'
        }
		return response


class UserView(APIView):
	permission_classes = (permissions.AllowAny,)
	def get(self, request):
		#raise AuthenticationFailed('teste')
		print("try to get")
		token = request.COOKIES.get('jwt')
		print("token = ", token)
		if not token:
			raise AuthenticationFailed('Unauthenticated')

		try:
			payload = jwt.decode(token,'secret', algorithms=['HS256'])
		except jwt.ExpiredSignatureError:
			raise AuthenticationFailed('Unauthenticated!')

		user = AppUser.objects.filter(user_id = payload['user_id']).first()
		serializer = UserSerializer(user)
		return Response(serializer.data, status=status.HTTP_200_OK)