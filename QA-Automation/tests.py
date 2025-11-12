# from django.test import TestCase
import pytest
from playwright.sync_api import Page, expect
from helpers import before_hook, create_task, delete_task_by_name, mark_task_completed, assert_tasks_on_page

def test_login(page: Page):
    before_hook(page, "user1", "password123") # Credentials should ideally be stored in .env file
    
    # Simple create and delete task
    create_task(page, "test task 1")
    delete_task_by_name(page, "test task 1")

    # Create, complete, delete task
    create_task(page, "test task 2")
    mark_task_completed(page, "test task 2")
    delete_task_by_name(page, "test task 2")

    # Create 2 pages worth of tasks
    for i in range(3,9):
        create_task(page, "test task " + str(i))

    # Check that the first 5 items are displayed on the current page
    assert_tasks_on_page(page, ["test task 8", "test task 7", "test task 6", "test task 5", "test task 4"])

    # Advance to the next page
    page.get_by_test_id("next-page").click()

    # Check for the remaining item
    assert_tasks_on_page(page, ["test task 3"])