from playwright.sync_api import Page, expect

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