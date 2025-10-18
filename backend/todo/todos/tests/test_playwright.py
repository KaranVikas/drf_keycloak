from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model
from playwright.sync_api import sync_playwright , Page, Browser, Playwright
from todo.todos.models import Todo

User = get_user_model()

class PlaywrightTestCase(StaticLiveServerTestCase):
  """ Base test case for playwright tests with Django """
  @classmethod
  def setUpClass(cls):
    # Start Django live server
    super().setUpClass()
    cls.playwright = sync_playwright().start()
    cls.browser = cls.playwright.chromium.launch(headless=True)

  @classmethod
  def tearDownClass(cls):
    cls.browser.close()
    cls.playwright.stop()
    super().tearDownClass()

  def setUp(self):
    # Set up test database
    super().setUp()
    self.context = self.browser.new_context()
    self.page = self.context.new_page()

  def tearDown(self):
    self.page.close()
    self.context.close()
    super().tearDown()

class TodoPlaywrightTest(PlaywrightTestCase):

  def setUp(self):
    super().setUp()
    # Create test user
    self.user = User.objects.create_user(
      username='user4',
      email='user4@gmail.com',
      password='password',
    )

  def login(self):
    """ Helper method to login user """
    self.page.goto(f'{self.live_server_url}/admin/login/')
    self.page.fill('input[name="username"]', 'user4')
    self.page.fill('input[name="password"]', 'password')
    self.page.click('input[type="submit"]')

  def test_page_loads(self):
     """ Test that the page loads successfully """
     self.page.goto(self.live_server_url)
     self.page.wait_for_load_state('networkidle')

     # check if the page load successfully
     self.assertIn('200', str(self.page.evaluate('() => document.readyState')))
