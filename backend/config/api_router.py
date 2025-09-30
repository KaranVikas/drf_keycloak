from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from todo.users.views import UserViewSet
from todo.todos.views import TodoViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("todos", TodoViewSet, basename="todos")

app_name = "api"
urlpatterns = router.urls
