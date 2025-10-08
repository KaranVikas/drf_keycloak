import logging
import uuid
from typing import Optional, Tuple
from urllib.parse import splitvalue
from django.conf import settings
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions
from django.contrib.auth import get_user_model
import jwt
from jwt import PyJWKClient
from .jwks import get_jwks

User = get_user_model()

logger = logging.getLogger(__name__)

class KeycloakJWTAuthentication(BaseAuthentication):
    """
    DRF Authentication that:
    - Extracts Bearer token
    - Validates signature with Keycloak realm JWKS (RS256)
    - Enforces iss, aud, exp (with leeway)
    Returns (user, token_payload) where user is a lightweight object.
    """

    www_authenticate_realm = "api"

    def authenticate(self, request) -> Optional[Tuple[object, dict]]:
        logger.info(f"=== AUTHENTICATION ATTEMPT ===")
        logger.info(f"Request path: {request.path}")
        logger.info(f"Request method: {request.method}")

        auth = get_authorization_header(request).split()

        logger.info(f"Auth header received: {auth}")
        logger.info(f"KEYCLOAK_JWKS_URL: {settings.KEYCLOAK_JWKS_URL}")
        logger.info(f"KEYCLOAK_ISSUER: {settings.KEYCLOAK_ISSUER}")
        logger.info(f"KEYCLOAK_AUDIENCE: {settings.KEYCLOAK_AUDIENCE}")
        logger.info(f"Token audience (aud) )))))))))): {settings.KEYCLOAK_AUDIENCE}")

        if not auth or auth[0].lower() != b"bearer":
          logger.warning(f"❌ No Bearer token found or wrong format")

          return None

        if len(auth) == 1:
            raise exceptions.AuthenticationFailed("Invalid Authorization header: No credentials provided.")
        elif len(auth) > 2:
            raise exceptions.AuthenticationFailed("Invalid Authorization header: Token string should not contain spaces.")

        raw_token = auth[1].decode("utf-8")
        logger.info(f"Token received: {raw_token[:50]}...")

        # For debugging token audience
        # try:
        #     # Decode WITHOUT verification to see token contents
        #     unverified_payload = jwt.decode(raw_token, options={"verify_signature": False})
        #     logger.info(f"Token contents: {unverified_payload}")
        #     logger.info(f"Token audience (aud): {unverified_payload.get('aud')}")
        #     logger.info(f"Token issuer (iss): {unverified_payload.get('iss')}")
        #     logger.info(f"Expected audience: {settings.KEYCLOAK_AUDIENCE}")
        #     logger.info(f"Expected issuer: {settings.KEYCLOAK_ISSUER}")
        # except Exception as e:
        #     logger.error(f"Could not decode token for debugging: {e}")

        # stop aud debugging

        logger.info(f"KEYCLOAK_JWKS_URL: {settings.KEYCLOAK_JWKS_URL}")

        # Use PyJWKClient correctly - point directly to JWKS URL
        jwk_client = PyJWKClient(settings.KEYCLOAK_JWKS_URL)

        try:
            logger.info(f"able to get jwk_client: {jwk_client}")
            logger.info(f"jwk_client: {raw_token[:50]}...")
            logger.info(f"signing_key start: {jwk_client.get_signing_key_from_jwt(raw_token)}")
            signing_key = jwk_client.get_signing_key_from_jwt(raw_token)
            logger.info(f"Successfully obtained signing key: {signing_key}")
        except Exception as e:
            logger.error(f"Unable to obtain signing key: {e}")
            raise exceptions.AuthenticationFailed(f"Unable to obtain signing key: {e}")

        try:
            payload = jwt.decode(
                raw_token,
                signing_key.key,
                algorithms=["RS256"],
                audience=settings.KEYCLOAK_AUDIENCE,
                issuer=settings.KEYCLOAK_ISSUER,
                leeway=settings.KEYCLOAK_LEEWAY,
                options={
                    "require": ["exp", "iat", "iss"],
                    "verify_aud": False,
                },
            )

            logger.info('token validation successful')
        except jwt.ExpiredSignatureError as e:
            logger.error(f"❌ Token has expired: {e}")
            raise exceptions.AuthenticationFailed("Token has expired.")
        except jwt.InvalidIssuerError as e:
          logger.error(f"❌ Invalid token issuer: {e}")
          logger.error(f"Expected issuer: {settings.KEYCLOAK_ISSUER}")
          raise exceptions.AuthenticationFailed("Invalid token issuer.")
        except jwt.InvalidAudienceError as e:
          logger.error(f"❌ Invalid token audience: {e}")
          logger.error(f"Expected audience: {settings.KEYCLOAK_AUDIENCE}")
          raise exceptions.AuthenticationFailed("Invalid token audience.")
        except Exception as e:
          logger.error(f"❌ JWT decode failed with error: {e}")
          logger.error(f"Error type: {type(e)}")
          raise exceptions.AuthenticationFailed(f"Token validation error: {e}")

        keycloak_id = payload.get("sub")
        username = payload.get("username") or payload.get("email") or keycloak_id
        email = payload.get("email","")
        name = payload.get("name", "")

        django_user = self.get_or_create_user(keycloak_id, username, email, name, payload)

        logger.info(f"✅ Authentication successful for user: {django_user.username} (ID: {django_user.id})")
        return (django_user, payload)

    def get_or_create_user(self, keycloak_id: str, username: str, email: str, name: str, payload: dict):
      """Get or create Django user from keycloak user"""
      try:
        # Try to find the user by keycloak ID first
        if keycloak_id:
          user = User.objects.get(keycloak_id=keycloak_id)
          logger.info(f"found existing user: {user.username }")

          #update user infonif changed
          updated = False
          if user.email != email and email:
            user.email = email
            updated = True

          if user.name !=name and name:
            user.name = name
            updated = True

          if updated:
            user.save()
            logger.info(f"Updated user info for: {user.username}")

          return user

      except User.DoesNotExist:
        pass

      try:
        # Try to find the user by username
        user = User.objects.get(username=username)
        logger.info(f"Found existing user: {user.username}")

        #Link with keycloak ID if not already linked
        if not user.keycloak_id and keycloak_id:
          user.keycloak_id = keycloak_id
          user.save()
          logger.info(f"Linked existing user: {user.username} with keycloak ID")

        return user

      except User.DoesNotExist:
        pass

      #Create new user
      try:
        user = User.objects.create(
          username=username,
          email=email,
          name=name,
          keycloak_id=keycloak_id,
          is_active=True,
        )
        logger.info(f"Created new Django user: {user.username} from keycloak user")
        return user
      except Exception as e:
        logger.error(f" Failed to create user: {e}")
        #If username already exists with different case or special characters,

        #create a unique username
        import uuid
        unique_username = f"{username}_{uuid.uuid4().hex[:8]}"
        user = User.objects.create(
          username=unique_username,
          email=email,
          name=name,
          keycloak_id=keycloak_id,
          is_active=True,
        )
        logger.info(f"Created new Django user with unique name: {user.username} ")
        return user

    def authenticate_header(self, request) -> str:
        return f'Bearer realm="{self.www_authenticate_realm}"'

# class KeycloakUser:
#     """
#     Minimal user object DRF can use. Mark as authenticated.
#     """
#     def __init__(self, sub: str, username: str, email: Optional[str], raw: dict):
#         self.id = sub
#         self.username = username
#         self.email = email
#         self._payload = raw
#
#     @property
#     def is_authenticated(self) -> bool:
#         return True

