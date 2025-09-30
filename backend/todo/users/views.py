from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

# added
from rest_framework.permissions import IsAuthenticated
from todo.auth_keycloak.authentication import KeycloakJWTAuthentication

from todo.users.models import User
#
# from todo.users.serializers import UserSerializer

# class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
#     serializer_class = UserSerializer
#     queryset = User.objects.all()
#     lookup_field = "username"
#
#     def get_queryset(self, *args, **kwargs):
#         assert isinstance(self.request.user.id, int)
#         return self.queryset.filter(id=self.request.user.id)
#
#     @action(detail=False)
#     def me(self, request):
#         serializer = UserSerializer(request.user, context={"request": request})
#         return Response(status=status.HTTP_200_OK, data=serializer.data)

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
