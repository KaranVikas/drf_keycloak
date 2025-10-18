"""
Step 1: Basic Test Infrastructure
Tests that Playwright and Django test server are working together.
"""
import os
import json
from IPython.core import page
from django.test import LiveServerTestCase
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout


class Step1BasicSetupTest(LiveServerTestCase):
  """
  Step 1: Verify basic Playwright + Django setup works.
  This is the foundation for all other tests.
  """

  def test_playwright_launches(self):
    """Test that Playwright can launch a browser."""
    with sync_playwright() as p:
      browser = p.chromium.launch(headless=True)
      print("Step 1.1: Browser launched successfully")

      page = browser.new_page()
      print("Step 1.2: New page created successfully")

      # Just verify we can create a page
      self.assertIsNotNone(page)

      page.close()
      browser.close()
      print("Step 1.3: Browser closed successfully")

  def test_django_server_accessible(self):
    """Test that Django test server is running and accessible."""
    with sync_playwright() as p:
      browser = p.chromium.launch(headless=True)
      page = browser.new_page()

      # Test Django admin (we know this exists)
      admin_url = f"{self.live_server_url}/admin/"
      print(f"Step 1.4: Django test server URL: {self.live_server_url}")

      response = page.goto(admin_url)
      print(f"Step 1.5: Admin page status: {response.status}")

      # Verify we got a successful response
      self.assertEqual(response.status, 200)

      # Verify the page has content
      title = page.title()
      print(f"Step 1.6: Admin page title: {title}")
      self.assertIn("Log in", title)

      browser.close()
      print("Step 1: All basic setup tests passed! ")

class step2FrontendConnectivityTest(LiveServerTestCase):
  """
  Step 2: Verify React frontend is running and accessible.
  Teste frontend on localhost:5173
  """

  # Frontend URL
  FRONTEND_URL = "http://10.0.0.236:5173/"

  def test_front_is_running(self):
    """ Test that front server is running and responding. """
    with sync_playwright() as p:
      browser = p.chromium.launch(headless=True)
      page = browser.new_page()

      print(f"Step 2.1: Attempting to connect to frontend at {self.FRONTEND_URL}")

      try:
        # Try to access the frontend with a reasonable timeout
        response = page.goto(self.FRONTEND_URL, timeout=10000)

        print(f" Step 2.2: Frontend responded with status: {response.status}")

        # Check for successful response (200) or cached response (304)
        self.assertIn(response.status, [200, 304], f"Expected 200 or 304, got {response.status}")

        # wait for page to be fully loaded
        page.wait_for_load_state('networkidle', timeout=5000)
        print(" Step 2.3: Frontend page fully loaded")

      except PlaywrightTimeout:
        print(f" step 2.2 Frontend not responding on {self.FRONTEND_URL}")
        print(f"Make sure frontend is running")
        self.fail(f"Frontend not accessible at {self.FRONTEND_URL}")

      except Exception as e:
        print(f" step 2.2:  Error connecting to frontend: {e}")
        raise

      finally:
        browser.close()

  def test_frontend_loads_content(self):
    """ Test that frontend loads actual content (not empty page). """
    with sync_playwright() as p:
      browser = p.chromium.launch(headless=True)
      page = browser.new_page()

      try:
        page.goto(self.FRONTEND_URL, timeout=10000)
        page.wait_for_load_state('networkidle', timeout=5000)

        #Get page title
        title = page.title()
        print(f" step 2.4: Page title: {title}")

        # # Verify title is not empty
        # self.assertIsNone(title, "Page title should not be None")

#         Get page content
        content = page.content()
        content_length = len(content)
        print(f"step 2.5 Page content length: {content_length} characters")

        # verify page has substainial content (more than just empty HTML)
        self.assertGreater(content_length, 100, "Page should have substantial content")

#         Check if React root div exists
        root_div = page.locator('#root')
        root_count = root_div.count()
        print(f" step 2.6: React root div found: {root_count > 0} ")

        if root_count > 0:
          print(" stop 2.7: React root div not found (might use different ID)")

        # else:
        #   print("step 2.7: React root div not found (might) use different ID ")

      except PlaywrightTimeout:
        print(f" Frontend not responding on {self.FRONTEND_URL}")
        self.fail(f"Frontend not accessible at {self.FRONTEND_URL}")

      finally:
        browser.close()

  def test_frontend_captures_screenshot(self):
    """ Test that we can capture screenshot of frontend. """
    with sync_playwright() as p:
      browser = p.chromium.launch(headless=True)
      page = browser.new_page()

      try:
        page.goto(self.FRONTEND_URL, timeout=10000)
        page.wait_for_load_state('networkidle', timeout=5000)

        # Take screenshot
        screenshot_path = 'test_screenshot_step2.png'
        page.screenshot(path=screenshot_path)

#           verify screenshot file was created
        screenshot_exists = os.path.exists(screenshot_path)
        print(f" step 2.8: Screenshot saved: {screenshot_path}")
        print(f" step 2.9: Screenshot exist: {screenshot_exists}")

        self.assertTrue(screenshot_exists, "Screenshot file was created at {screenshot_path}")

      except PlaywrightTimeout:
        print(f" Frontend not responding on {self.FRONTEND_URL}")
        self.fail(f"Frontend not accessible at {self.FRONTEND_URL}")

      finally:
        browser.close()

  def test_frontend_body_text_accessible(self):
    """ Test that we can read text content from the frontend. """
    with sync_playwright() as p:
      browser = p.chromium.launch(headless=True)
      page = browser.new_page()

      try:
        page.goto(self.FRONTEND_URL, timeout=10000)
        page.wait_for_load_state('networkidle', timeout=5000)

        #Get body text count
        body_text = page.text_content('body')
        print(f"Step 2.11: Body text length: {len(body_text)} characters")

        # Show preview of content
        preview = body_text[:200] if body_text else ""
        print(f"✅ Step 2.12: Content preview: {preview}...")

        # Verify there's actual text content
        self.assertIsNotNone(body_text, "Body should have text content")
        self.assertGreater(len(body_text), 0,
                           "Body should have some text content")

        print("✅ Step 2: All frontend connectivity tests passed! ✅")

      except PlaywrightTimeout:
        print(f" Frontend not responding on {self.FRONTEND_URL}")
        self.fail(f"Frontend not accessible at {self.FRONTEND_URL}")
      finally:
        browser.close()

class Step3KeycloakConnectivityTest(LiveServerTestCase):
  """
    Step3 : Verify Keycloak is running and accessible.
    Test keyecloak on localhost:8080
  """

  #keycloak URL
  KEYCLOAK_URL = "http://10.0.0.236:8080/"
  KEYCLOAK_REALM = "todo"

  def test_keycloak_is_running(self):
    """ Teste that keycloak is running and responding. """
    with sync_playwright() as p:
      browser = p.chromium.launch(headless=True)
      page = browser.new_page()

      print(f"  step 3.1: Attempting to connect to keycloak at {self.KEYCLOAK_URL}")

      try:
#       Try to access keycloak homepage
        response = page.goto(self.KEYCLOAK_URL, timeout=10000)

        print(f" step 3.2: Keycloak responded with status: {response.status}")

#       Check for successful response
        self.assertEqual(response.status, 200 , f"Expected 200, got {response.status}")

        # wait for page to load
        page.wait_for_load_state('networkidle', timeout=5000)
        print(" step 3.3: Keycloak page fully loaded")

      except PlaywrightTimeout:
        print(f" step 3.2 Keycloak not responding on {self.KEYCLOAK_URL}")
        print(f"Make sure keycloak is running")
        self.fail(f"Keycloak not accessible at {self.KEYCLOAK_URL}")

      except Exception as e:
        print(f" step 3.2 Error connecting to keycloak: {e}")
        raise

      finally:
        browser.close()

  def test_keycloak_welcome_page(self):
    """ Test that keycloak welcome/admin page loads. """
    with sync_playwright() as p:
      browser = p.chromium.launch(headless=True)
      page = browser.new_page()

      try:
        page.goto(self.KEYCLOAK_URL, timeout=10000)
        page.wait_for_load_state('networkidle', timeout=5000)

#           Get page title
        title = page.title()
        print(f"step 3.4: Keycloak page title: '{title}'")

#           Check for keycloak-specific text
        self.assertIn("Keycloak", title, "Page title should contain 'Keycloak'")

#           Get page content
        content = page.content()
        print(f"Step 3.5: Page content length: {len(content)} characters")

#           Check for keycloak-specific text
        body_text = page.text_content('body')
        print(f" step 3.6: Body text preview: {body_text[:200]}...")

#             Take screenshot
        screenshot_path = 'test_screenshot_keycloak.png'
        page.screenshot(path=screenshot_path)
        print(f" step 3.7: Screenshot saved: {screenshot_path}")

      except PlaywrightTimeout:
        print(f" keycloak not responding on {self.KEYCLOAK_URL}")
        self.fail(f"keycloak not accessible at {self.KEYCLOAK_URL}")

      finally:
        browser.close()

  def test_keycloak_admin_console_accessible(self):
    """ Test that keycloak admin console is accessible. """
    with sync_playwright() as p:
      browser = p.chromium.launch(headless=True)
      page = browser.new_page()

      try:
#             Access admin console
        admin_url = f"{self.KEYCLOAK_URL}/admin/"
        print(f" step 3.8: Accessing admin console: {admin_url}")

        response = page.goto(admin_url, timeout=10000)
        print(f" step 3.9: Admin console.status: {response.status}")

        # should get 200 (might redirect to login)
        self.assertEqual(response.status, 200)

        page.wait_for_load_state('networkidle', timeout=5000)

#       Check if we're on admin login page
        current_url = page.url
        print(f"step 3.10: Current URL: {current_url}")

#       should be redirected to admin console(might be login)
        self.assertIn("admin", current_url.lower(),
                      "should be on admin-related page")

        # Take screenshot of admin console]
        screenshot_path = 'test_screenshot_keycloak_admin.png'
        page.screenshot(path=screenshot_path)
        print(f" step 3.11: Admin screenshot saved: {screenshot_path}")

      except PlaywrightTimeout:
        print(f" Keycloak admin console not responding")
        self.fail(f"keycloak admin not accessible at {admin_url}")

      finally:
        browser.close()

  def test_keycloak_realm_endpoint(self):
    """ Test that the todo realm is configured and accessible. """

    with sync_playwright() as p:
      browser = p.chromium.launch(headless=True)
      page = browser.new_page()

      try:
#       Access realm metadata endpoint
        realm_url = f"{self.KEYCLOAK_URL}/realms/{self.KEYCLOAK_REALM}"
        print(f" step 3.12: Accesssing realm: {realm_url}")

        response = page.goto(realm_url, timeout=10000)
        print(f" step 3.13: Realm enpoint status: {response.status}")

#       Realm endpoint should return 200
        self.assertEqual(response.status ,200)

        #Get the JSON response
        content = page.content()

#       The page should contain JSON data about the realm
        self.assertIn("realms", content.lower(), 'response should contain realm information')

        print(f"Step 3.14 Realm '{self.KEYCLOAK_REALM}' is configured")

      except PlaywrightTimeout:
        print(f" Realm endpoint not responding")
        print(f"Make sure realm '{self.KEYCLOAK_REALM}' is configured")
        self.fail(f"Realm endpoint not accessible at {realm_url}")

      except Exception as e:
        print(f" step 3.12 Erorr accessing realm: {e}")
        raise

      finally:
        browser.close()

  def test_keycloak_openid_connection(self):
    """ Test that OpenID connect configuration is available."""

    with sync_playwright() as p:
      browser = p.chromium.launch(headless=True)
      page = browser.new_page()

      try:
#       Access OpenID configuration endpoint
        oidc_url = f"{self.KEYCLOAK_URL}/realms/{self.KEYCLOAK_REALM}/.well-known/openid-configuration"
        print(f" Step 3.15: Accessing OIDC config: {oidc_url}")

        response = page.goto(oidc_url, timeout=10000)
        print(f" Step 3.16: OIDC config status: {response.status}")

        self.assertEqual(response.status, 200)

#       Get the JSON content
        content = page.text_content('body')

#       Parse JSON to verify it;s valid
        try:
          oidc_config = json.loads(content)
          print(f" step 3.17: OIDC config loaded successfully")

#         Check for the important OIDC endpoints
          expected_keys = ['authorization_endpoint', 'token_endpoint', 'userinfo_endpoint']
          for key in expected_keys:
            self.assertIn(key, oidc_config, f"OIDC config should contain '{key}'")

            print(f" Step 3.18: Found '{key}:{oidc_config[key][:80]}...' in OIDC config")

          print(f"Step 3.19 OIDC endpoints configured correctly")

        except json.JSONDecodeError as e:
          print(f" Invalid JSON in OIDC configuration: {e}")
          self.fail("OIDC configuration is not valid JSON")

      except PlaywrightTimeout:
        print(f" OIDC configuration endpoint not responding")
        self.fail(f"OIDC configuration endpoint not accessible at {oidc_url}")

      except Exception as e:
        print(f" Error accesssing OIDC config: {e}")
        raise

      finally:
        browser.close()

  def test_keycloak_jwks_endpoint(self):
    """ Test that JWKS endpoint is available. """
    with sync_playwright() as p:
      browser = p.chromium.launch(headless=True)
      page = browser.new_page()

      try:
    #     Access JWKs endpoint
        jwks_url = f"{self.KEYCLOAK_URL}/realms/{self.KEYCLOAK_REALM}/protocol/openid-connect/certs"
        print(f" Step 3.20: Accessing JWKS: {jwks_url}")

        response = page.goto(jwks_url, timeout=10000)
        print(f" Step 3.21: JWKS endpoint status: {response.status}")

    #     should return 200
        self.assertEqual(response.status, 200)

    #     Get the JSON content
        content = page.text_content('body')

    #     Parse Json to verify it;s valid
        try:
          jwks_data = json.loads(content)
          print(f" Step 3.22: JWKS loaded successfully")

    #       Check for keys arrays
          self.assertIn('keys', jwks_data, 'JWKS should contain keys array')

          keys_count = len(jwks_data['keys'])
          print(f" Step 3.23: Found {keys_count} signing key(s)")

          self.assertGreater(keys_count, 0, "JWKS should contain at least one key")

          print(f"Step 3.3 All keycloak connectivity tests passed! ")

        except json.JSONDecodeError as e:
          print(f" Invalid JSON in JWKS: {e}")
          self.fail("JWKS is not valid JSON")

      except PlaywrightTimeout:
        print(f" JWKS endpoint not responding")
        self.fail(f"JWKS endpoint not accessible at {jwks_url}")

      except Exception as e:
        print(f" Error accessing JWKS: {e}")
        raise

      finally:
        browser.close()













