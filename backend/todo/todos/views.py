from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from todo.auth_keycloak.authentication import KeycloakJWTAuthentication
from .models import Todo
from .serializers import TodoSerializer, TodoCreateSerializer

class TodoViewSet(ModelViewSet):
  """
  Simple Todo Viewset with CRUD operations
  """

  """
  Endpoints:

  """

  authentication_classes = [KeycloakJWTAuthentication]
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
    """
    use different serializers for different actions
    """
    if self.action == 'create':
      return TodoCreateSerializer
    return TodoSerializer

  def create(self, request, *args, **kwargs):
    """
    Create a new todo for the authenticated user
    """

    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    #Save with user_sub from JWT token

    todo = serializer.save(user_sub = request.user.id)

    #Return full todo data
    response_serializer = TodoSerializer(todo)
    return Response(response_serializer.data, status=status.HTTP_201_CREATED)

  def update(self, request, *args, **kwargs):
    todo = get_object_or_404(Todo, id=kwargs['pk'], user_sub = request.user.id)

    serializer = TodoSerializer(todo, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data)

  def destory(self, request, *args, **kwargs):
    todo = get_object_or_404(Todo, id=kwargs['pk'], user_sub = request.user.id)
    todo.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

  def list(self, request, *args, **kwargs):
    """
      List all todos for the authenticated user
    """
    queryset = self.get_queryset()
    serializer = TodoSerializer(queryset , many=True)

    return Response({
      'count': queryset.count(),
      'results': serializer.data
    })




