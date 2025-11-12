# from django.test import TestCase
import pytest
from playwright.sync_api import Page, expect
from helpers import before_hook, create_task, delete_task_by_name, mark_task_completed, assert_tasks_on_page, logout, login, cleanup_previous_tasks

def test_functionality(page: Page):
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

    # Log out and check that a different user cannot see any of user1's tasks
    logout(page)
    login(page, "user2", "password321")

    # Assert only expected items found
    assert_tasks_on_page(page, ["this is the only user2 task"])
    expect(page.get_by_test_id("task-list").locator("> [data-testid='list-element']")).to_have_count(1)

    """
        NOTE: Test will start failing, if someone accidentally creates 
        any tasks or deletes the expected one on user2.
    """

    # Now sign back into user1 to assert task permanence
    logout(page)
    login(page, "user1", "password123")

    assert_tasks_on_page(page, ["test task 8", "test task 7", "test task 6", "test task 5", "test task 4"])
    page.get_by_test_id("next-page").click()
    assert_tasks_on_page(page, ["test task 3"])

    # Finally, clean the test environment
    cleanup_previous_tasks(page)