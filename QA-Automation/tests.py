# from django.test import TestCase
import pytest
from playwright.sync_api import Page, expect
from helpers import before_hook, create_task, delete_task_by_name

def test_login(page: Page):
    
    before_hook(page, "user1", "password123") # Credentials should ideally be stored in .env file
    create_task(page, "testtask")
    delete_task_by_name(page, "testtask")