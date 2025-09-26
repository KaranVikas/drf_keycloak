# Validation middleware
"""
JWT validationn middleware
Validates keycloak JWT tokens and extracts user information
"""

import jwt
import requests
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin

User = get_user_model()

class KeycloakJWTMiddleware(MiddlewareMixin):

  """
  Middleware to validate JWT tokens from keycloak
  Extracts user information from token and creates/updates Django user.
  """

  def process_request(self, request):
      # skip validation for non-api endpoints
      if not request.path.startswith('/api/'):
          return None

      #skip validation for public endpoints
      public_endpoints = ['/api/auth/health','/api/docs/']
      if any(request.path.startswith(endpoint) for endpoints in public_endpoints):
          return None

      auth_header = request.META.get('HTTP_AUTHORIZATION')
      if not auth_header or not auth_header.startswith('Bearer '):
          return JsonResponse({'error':'Authorization header required'},status=401)

      token = auth_header.split(' ')[1]

      decoded_token = self._validate_token(token)
      if decoded_token:
        user = self._get_or_create_user(decoded_token)
        request.user = user
        request.keycloak_token = decoded_token

      return None

  def _validate_token(self, token):
    """ Validate JWT token with keycloak public key """
    try:
      #Get public key from cache or fetch from keycloak
      public_key = self._get_public_key()

      # Decode and validate token

      decoded_token = jwt.decode(
        token,
        public_key,
        algorithms=['RS256'],
        audience=settings.KEYCLOAK_CLIENT_ID,
        issuer= settings.KEYCLOAK_ISSUER
      )
      return decoded_token
    except jwt.InvalidTokenError:
        return None

  def _get_public_key(self):
    """Get Keycloak public key (cached for performance)"""
    cache_key = 'keycloak_public_key'
    public_key = cache.get(cache_key)

    if not public_key:
      try:
        # Fetch from Keycloak well-known endpoint
        well_known_url = f"{settings.KEYCLOAK_ISSUER}/.well-known/openid-configuration"
        response = requests.get(well_known_url)
        jwks_uri = response.json()['jwks_uri']

        # Get public keys
        jwks_response = requests.get(jwks_uri)
        public_key = jwks_response.json()['keys'][0]

        # Cache for 1 year
        cache.set(cache_key, public_key, timeout=365 * 24 * 60 * 60)
      except Exception:
        return None

    return public_key

  def _get_or_create_user(self, token_data):
    """Get or create Django user from keycloak token"""

    username = user_info.get('preferred_username')
    email = user_info.get('email','')

    user, created = User.objects.get_or_create(
      username=username,
      defaults={
        'email':email,
      }
    )

    return user




