# from django.test import TestCase
import pytest
from playwright.sync_api import Page, expect
from helpers import login

def test_login(page: Page):
    # TODO: before hook
    page.goto("http://127.0.0.1:8000/login/")

    login(page, "user1", "hello", False)
    login(page, "user1", "password123")