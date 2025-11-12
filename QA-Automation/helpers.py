from playwright.sync_api import Page, expect, Locator
import datetime

def login(page: Page, username, password, validLogin = True):
    # Ensure we are on the right page
    expect(page).to_have_title('Login - Todo App')

    # Fill out information
    page.get_by_test_id("username-input").fill(username)
    page.get_by_test_id("password-input").fill(password)

    # Ensure login button is correctly displayed
    loginB = page.get_by_test_id("login-button")
    expect(loginB).to_be_visible()
    expect(loginB).to_contain_text("Login")

    # Submit login
    loginB.click()

    """
        NOTE: I want to validate successful login attempts, but I may also want to test invalid attempts too. 
        Instead of having a separate function for that, or retyping the login logic for failing paths, I
        added this branch to allow for both.
    """
    if(validLogin):
        expect(page).to_have_title('Dashboard - Todo App')

    else:
        expect(page.get_by_text("Invalid username or password.")).to_be_visible()

"""
    Previous tests may have failed and left unwanted tasks behind. To prevent test-interferance with previous
    attempts, first check to see if there are any unwanted items, then delete any that are found.
"""
def cleanup_previous_tasks(page: Page):
    # Ensure we are on the correct page
    expect(page).to_have_title('Dashboard - Todo App')

    # Get task list and check for any children
    taskList = page.get_by_test_id("task-list")
    children = taskList.locator("> [data-testid='list-element']") # Get all relevant children
    
    # If there are any leftover tasks from previous tests, delete these
    while(children.count() > 0):
        delete_task(page, children.nth(0))
        children = taskList.locator("> [data-testid='list-element']") # Get all relevant children

    # Ensure all elements have been successfully deleted
    expect(children).to_have_count(0)
    expect(page.get_by_text("No tasks yet. Add your first task above!")).to_be_visible()

def delete_task(page: Page, element):
    element.locator("> [data-testid='list-element-options']").locator("> [data-testid='list-element-delete']").click()
    expect(page.get_by_text("Task deleted successfully!")).to_be_visible()

def delete_task_by_name(page: Page, elementName: str):
    element = page.get_by_test_id("list-element-title").get_by_text(elementName)
    expect(element).to_have_count(1)

    """ I would much more prefer to use the Cypress style .parents(<selector>), since xpath is bad practice """
    delete_task(page, element.locator("xpath=../.."))

"""
    Collection of helper functions that need to run before most (if not all) tests.
"""
def before_hook(page: Page, username, password):
    # Visit baseurl (ideally an env variable)
    page.goto("http://127.0.0.1:8000/login/")

    # Log in
    login(page, username, password)

    # Ensure clean environment to run test
    cleanup_previous_tasks(page)

def create_task(page: Page, taskName):

    # Create new task
    page.get_by_test_id("new-task-name-input").fill(taskName)
    page.get_by_test_id("new-task-create-button").click()
    time = datetime.datetime.now().strftime("%b %d, %Y %H:%M") # Save time for verification later

    # Assert new task has been created
    expect(page.get_by_text("Task added successfully!")).to_be_visible()
    newTask = page.get_by_test_id("task-list").locator("> [data-testid='list-element']").nth(0)

    # Check name of new task
    expect(newTask.locator("[data-testid='list-element-title']").nth(0)).to_have_text(taskName) 

    # Check details of new task
    userName = page.get_by_test_id("user-greeting").text_content() # This gets "Hello, <user>!" and extracts the username
    userName = userName[7:]
    userName = userName[:-1]

    """
        Very unlikely flake - should the submission of task and getting date fall in different minutes
        this test will fail. In the future, this should also check for incremented time.
    """
    expect(newTask.locator("[data-testid='list-element-info']").nth(0)).to_have_text("Created by: " + userName + " | " + time)
