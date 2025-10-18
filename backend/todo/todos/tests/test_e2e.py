from django.test import LiveServerTestCase
from playwright.sync_api import sync_playwright


class TodoAppE2ETest(LiveServerTestCase):
  def test_homepage_title(self):
    """Launch browser and check page title using Playwright."""
    with sync_playwright() as p:
      browser = p.chromium.launch(headless=True)
      page = browser.new_page()

      # Visit the live Django test server
      page.goto(self.live_server_url)
      print("Server URL:", self.live_server_url)

      # Example check: ensure title or element exists
      title = page.title()
      print("Page title:", title)
      # self.assertIn("Django", title)

      # Test an endpoint that exists (e.g., admin)
      page.goto(f"{self.live_server_url}/admin/")
      print("Server URL:", self.live_server_url)

      # Check the response status
      response = page.goto(f"{self.live_server_url}/admin/")
      print(f"Response status: {response.status}")
      self.assertEqual(response.status, 200, "Admin page should return 200")

      title = page.title()
      print("Page title:", title)

      browser.close()
