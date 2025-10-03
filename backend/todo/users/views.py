from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

# added
from rest_framework.permissions import IsAuthenticated
from todo.auth_keycloak.authentication import KeycloakJWTAuthentication

from todo.users.models import User
from .serializers import UserSerializer, UserRegisterationSerializer

# Get the User Model
User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
  """
  Register a new user
  """
  serializer = UserRegisterationSerializer(data=request.data)
  if serializer.is_valid():
    user = serializer.save()
    return Response(
      UserSerializer(user).data,
      status=status.HTTP_201_CREATED
    )

class UserViewSet(GenericViewSet):
  authentication_classes = [KeycloakJWTAuthentication]
  permission_classes = [IsAuthenticated]

  queryset = User.objects.none()

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
