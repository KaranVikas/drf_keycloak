from typing import Optional, Tuple
from urllib.parse import splitvalue
from django.conf import settings
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions
import jwt
from jwt import PyJWKClient
from .jwks import get_jwks

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
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != b"bearer":
            return None

        if len(auth) == 1:
            raise exceptions.AuthenticationFailed("Invalid Authorization header: No credentials provided.")
        elif len(auth) > 2:
            raise exceptions.AuthenticationFailed("Invalid Authorization header: Token string should not contain spaces.")

        raw_token = auth[1].decode("utf-8")

        # Prepare JWK client from cached JWKS (avoid network for each request)
        jwks = get_jwks()
        jwk_client = PyJWKClient.from_jwks_data(jwks)

        try:
            signing_key = jwk_client.get_signing_key_from_jwt(raw_token)
        except Exception as e:
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
                },
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token has expired.")
        except jwt.InvalidIssuerError:
            raise exceptions.AuthenticationFailed("Invalid token issuer.")
        except jwt.InvalidAudienceError:
            raise exceptions.AuthenticationFailed("Invalid token audience.")
        except Exception as e:
            raise exceptions.AuthenticationFailed(f"Token validation error: {e}")

        # Build a lightweight user object (no DB hit). You can plug your User model here if desired.
        user = KeycloakUser(
            sub=payload.get("sub"),
            username=payload.get("preferred_username") or payload.get("email") or payload.get("sub"),
            email=payload.get("email"),
            roles=self._extract_realm_roles(payload),
            raw=payload,
        )
        return (user, payload)

    def authenticate_header(self, request) -> str:
        return f'Bearer realm="{self.www_authenticate_realm}"'

    @staticmethod
    def _extract_realm_roles(payload: dict):
        # Standard place: realm_access.roles
        try:
            return payload.get("realm_access", {}).get("roles", []) or []
        except Exception:
            return []


class KeycloakUser:
    """
    Minimal user object DRF can use. Mark as authenticated.
    """
    def __init__(self, sub: str, username: str, email: Optional[str], roles: list[str], raw: dict):
        self.id = sub
        self.username = username
        self.email = email
        self.roles = roles
        self._payload = raw

    @property
    def is_authenticated(self) -> bool:
        return True

    # Optional helpers for permissions
    def has_role(self, role: str) -> bool:
        return role in (self.roles or [])
