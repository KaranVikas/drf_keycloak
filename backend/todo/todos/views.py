import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Todo
from todo.authentication.views import TokenRequiredMixin


@method_decorator(csrf_exempt, name='dispatch')
class TodoListView(TokenRequiredMixin, View):
  """
    Handle Todo list operations
    GET: List user's todos
    POST: Create new todo
  """

  def get(self, request):
    todos = Todo.objects.filter(user=request.user)
    data = [{
      'id': str(todo.id),
      'title': todo.title,
      'completed': todo.completed,
      'created_at': todo.created_at.isoformat()
    } for todo in todos ]
    return JsonResponse(data, safe=False)

  def post(self, request):
    data = json.loads(request.body)
    todo = Todo.objects.create(
      title=data['title'],
      completed=data.get('completed', False),
      user=request.user
    )
    return JsonResponse({
      'id': str(todo.id),
      'title': todo.title,
      'completed': todo.completed,
      'created_at': todo.created_at.isoformat()
    })

  @method_decorator(csrf_exempt, name='dispatch')
  class TodoDetailView(TokenRequiredMixin, View):
    """
      Handle indiviaual Todo operations
      PUT: Update todo
      DELETE: Delete todo
    """

    def put(self, request, todo_id):
      try:
        todo = Todo.objects.get(id=todo_id, user=request.user)
        data = json.loads(request.body)

        todo.title = data.get('title', todo.title)
        todo.completed = data.get('completed', todo.completed)
        todo.save()

        return JsonResponse({
          'id': str(todo_id),
          'title': todo.title,
          'completed': todo.completed,
          'created_at': todo.created_at.isoformat()
        })
      except Todo.DoesNotExist:
        return JsonResponse({
          'error':'todo not found'
        }, status=404)

    def delete(self, request, todo_id):
      try:
        todo = Todo.objects.get(id=todo_id, user= request.user)
        todo.delete()
        return JsonResponse({'message':'Todo deleted'})
      except:
        return JsonResponse({'error':'Todo not found'}, status=404)
