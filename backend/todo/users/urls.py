from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
urlpatterns = [
  path("register/", views.register_user, name='register'),
  path('', include(router.urls)),
]
