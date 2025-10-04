from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

# added
from rest_framework.permissions import IsAuthenticated
from todo.auth_keycloak.authentication import KeycloakJWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model

from todo.users.models import User
from .serializers import UserSerializer, UserRegisterationSerializer

# Get the User Model
User = get_user_model()

class UserViewSet(GenericViewSet):
  authentication_classes = [KeycloakJWTAuthentication]
  permission_classes = [IsAuthenticated]
  serializer_class = UserSerializer

  def get_queryset(self):
    return User.objects.all()

  @action(detail=False, methods=['post'], url_path='register', permission_classes=[AllowAny])
  def register(self, request):
    """Register a new user"""
    serializer = UserRegisterationSerializer(data=request.data)
    if serializer.is_valid():
      user = serializer.save()
      return Response(
        UserSerializer(user).data,
        status=status.HTTP_201_CREATED
      )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  @action(detail=False, methods=['get'], url_path='me')
  def me(self, request):
    """Get current user information from JWT token"""
    # Since you're using KeycloakUser, the user object is available in request.user
    user_data = {
      'id': request.user.id,
      'username': request.user.username,
      'email': request.user.email,
      'sub': request.user.id,
      # 'raw_token': request.user._payload
      # Full JWT payload if needed
    }
    return Response(user_data)
