import pytest
from django.contrib.auth import get_user_model
from django.url import reverse

User = get_user_model()

# verify the unauthenticated users see the correct login and registration UI.
@pytest.mark.django_db
@pytest.mark.e2e
def test_todo_app_authentication(page, live_server_url):
  """ Test the authentication flow to the Todo app """

#   Naavigate to the home page
  page.goto(f"{live_server_url}")

#   Check if the login button is present ( for unauthenticated users)
  login_button = page.locator("button:has-text('Login with KC)")
  assert login_button.is_visible()

#   check if register button is present
  register_button = page.locator("button:has-text(('Register with Keycloak')")
  assert register_button.is_visible()

#   verify the page title
  page_title = page.locator('h1')
  assert page_title.inner_text() == "Todo App"

@pytest.mark.django_db
@pytest.mark.e2e
def test_authenticated_user_view(page, live_server_url):
  """ Test the authenticated user view. """

#    Create a test user
  user = User.objects.get(
    username="",
    password="",
  )


@pytest.amrk.django_db
@pytest.mark.e2e
def test_api_endpoint(page, live_server_url):
  """ Test API endpoints accessibility. """
#   Test API endpoint  directly



