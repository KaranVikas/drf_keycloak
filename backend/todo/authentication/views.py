from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

@method_decorator(csrf_exempt, name='dispatch')
class TokenRequiredMixin:
  """ Mixin to require valid token for API access """
  def dispatch(self, request, *args, **kwargs):
    if not hasattr(request, 'keycloak_token'):
      return JsonResponse({'error': 'Invalid token'}, status=401)
    return super().dispatch(request, *args, **kwargs)

class ProfileView(TokenRequiredMixin, View):
  """
  Returns user profile information from keycloak token
  Endpoint: Get /api/auth.profile
  """

  def get(self, request):
    token_data = request.keycloak_token
    profile = {
      'username': token_data.get('preferred_username'),
      'email': token_data.get('email'),
      'first_name': token_data.get('first_name'),
      'last_name': token_data.get('last_name'),
      'roles': token_data.get('realm_access', {}).get('roles', [])
    }
    return JsonResponse({'profile': profile})
