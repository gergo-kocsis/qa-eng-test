from playwright.sync_api import Page, expect

def login(page: Page, username, password):
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
    