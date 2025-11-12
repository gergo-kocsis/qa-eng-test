# from django.test import TestCase
import pytest
from playwright.sync_api import Page, expect
from helpers import login

def test_login(page: Page):
    page.goto("http://127.0.0.1:8000/login/")

    # Ensure we are on the right page
    login(page, "user1", "password123")