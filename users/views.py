from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
import logging


# Create a logger for the users app
logger = logging.getLogger('users')


# For user registration
@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    # checking if username and password are provided or not
    if not username or not password:
        logger.error("Registration failed: Missing username or password")
        return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.create_user(username=username, password=password)
        logger.info(f"User registered successfully: {username}")
        return Response({"message": "User created"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(f"Error during registration: {str(e)}")
        return Response({"error": "User registration failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# For user login
@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    # checking if username and password are provided or not
    if not username or not password:
        logger.error("Login failed: Missing username or password")
        return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.filter(username=username).first()
    
    # checking if password is correct or not
    if user and user.check_password(password):
        refresh = RefreshToken.for_user(user)
        logger.info(f"User logged in successfully: {username}")
        
        # returning refresh and access tokens in response
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    
    logger.error(f"Login failed: Invalid credentials for username {username}")
    return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

