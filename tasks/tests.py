# from django.test import TestCase
import pytest
from playwright.sync_api import Page, expect

def test_login(page: Page):
    page.goto("http://127.0.0.1:8000/login/")
    page.fill('input[name="username"]', 'user1')
    page.fill('input[name="password"]', 'testpass123')
    page.click('button[type="submit"]')
    expect(page).to_have_url("http://127.0.0.1:8000/dashboard/")