from rest_framework import serializers
from .models import Todo

class TodoSerializer(serializers.ModelSerializer):
  """
    Serializer for Todo CRUD operations
  """
  username = serializers.CharField(source='user.username', read_only=True)

  class Meta:
    model = Todo
    fields = [
      'id',
      'title',
      'description',
      'completed',
      'created_at',
      'updated_at',
      'username'
    ]

    read_only_fields = ['id', 'created_at', 'updated_at','username']

  def validate_title(self, value):
    """Ensuring title is not empty after stripping whitespace """

    if not value.strip():
      raise serializers.ValidationError("Title cannot be empty")
    return value.strip()

class TodoCreateSerializer(serializers.ModelSerializer):
  """ Simplifies serializer for creating todos """

  class Meta:
    model = Todo
    fields = ['title','description']

  def validate_title(self, value):
    if not value.strip():
      raise serializers.ValidationError('Title cannot be empty')
    return value.strip()
