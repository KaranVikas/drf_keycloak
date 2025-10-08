from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

class Todo(models.Model):
  """
  Simple todo model to create CRUD operations
  Links to keycloak user via (subject) field
  """
  user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name='todos',
    help_text=_('The user who owns this todo')
  )

  #link to keycloak user (no foreign key to user model)
  user_sub = models.CharField(
    max_length=255,
    help_text="Keycloak user subject (sub claim from JWT)"
  )

  # Todo fields
  title = models.CharField(max_length=200)
  description = models.TextField(blank=True)
  completed = models.BooleanField(default=False)

  #Timestamps
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    ordering = ["-created_at"]
    # indexes = [
    #   # fast user lookup
    #   models.Index(fields=['user_sub']),
    # #   fast status filtering
    #   models.Index(fields=['completed']),
    # ]

  def __str__(self):
    return f"{self.title} - {'' if self.completed else 'O'}"

