import time
from typing import Optional
import requests
from django.core.cache import cache
from django.conf import settings

CACHE_KEY = "keycloak_jwks_cache"
CACHE_TTL = 60 * 15  # 15 minutes

def get_jwks(force: bool = False) -> dict:
    """
    Fetch and cache the JWKS from Keycloak realm. Mirrors the article's approach:
    pull realm certs and use them to validate RS256 JWTs.
    """
    if not force:
        jwks = cache.get(CACHE_KEY)
        if jwks:
            return jwks

    resp = requests.get(settings.KEYCLOAK_JWKS_URL, timeout=5)
    resp.raise_for_status()
    jwks = resp.json()
    cache.set(CACHE_KEY, jwks, CACHE_TTL)
    return jwks

# Preload JWKS during startup
def warm_jwks_cache() -> None:
    try:
        get_jwks(force=True)
    except Exception:
        # avoid hard-fail on startup; logs or Sentry hook can be added
        pass
