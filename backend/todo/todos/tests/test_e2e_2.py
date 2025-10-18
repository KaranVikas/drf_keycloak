"""
Step 1: Basic Test Infrastructure
Tests that Playwright and Django test server are working together.
"""
import os

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










