from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
urlpatterns = [
  path("register/", views.UserViewSet.as_view({'post':'register'}), name='register'),
  path('me/', views.UserViewSet.as_view({'get':'me'}), name='me'),
  path('', include(router.urls)),
]
