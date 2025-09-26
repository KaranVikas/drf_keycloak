from django.urls import path
from .views import ProfileView

app_name = 'authentication'

urlpatterns = [
  path('profile/', ProfileView.as_view(), name='profile'),
]
