import pytest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def playwright():
  """ Initialize the playwright for the test session"""
  with sync_playwright() as p:
    yield p

@pytest.fixture(scope="session")
def browser_type(playwright):
  """ Return browser type (chromium by default) """
  return playwright.chromium

@pytest.fixture(scope="session")
def browser(browser_type):
  """ Launch browser for the test session """
  browser = browser_type.launch(headless=True)
  yield browser
  browser.close()

@pytest.fixture(scope="session")
def page(browser):
  """ Create a new page for each test """
  context = browser.new_context()
  page = browser.new_page()
  yield page
  context.close()

@pytest.fixture
def live_server():
  """ Return the live server URL for Django """
  return live_server.url
