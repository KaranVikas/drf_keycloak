import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Todo(models.Model):
  """
    Simple Todo model linked to authenticated users.
    Each todo belongs to a specific user from keycloak.
  """

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  title = models.CharField(max_length=255)
  completed = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_new=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos')

  class Meta:
    ordering = ['-created_at']

  def __str__(self):
    return f"{self.title} - {self.user.username}"
