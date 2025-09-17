import pytest
import logging
from Project1_Guvi_Automation.config_reader import get_config
from Project1_Guvi_Automation.pages.home_page import Home_Page
from Project1_Guvi_Automation.pages.login_page import Login_Page
from Project1_Guvi_Automation.pages.dashboard_page import Dashboard_Page
from Project1_Guvi_Automation.pages.signup_page import Signup_Page
import time

# Set up logger for this test module
logger = logging.getLogger(__name__)

@pytest.mark.usefixtures("setup")
class Test_Guvi_Automation_Page:
    """
        Test Suite for GUVI Automation Page
        Verifies that the GUVI home page loads correctly and logs all steps validate neccessary fields,
        registeration login and logout
        """

    def test_tc1_validate_url(self, setup):
        """
               Test Case 1: Verify whether the given GUVI URL loads successfully.
               This test navigates to the GUVI homepage, retrieves the current
               page URL, and verifies it matches the expected URL from the config file.
               On success, it logs the actual URL and saves a screenshot.
               On failure, it logs the error and saves a screenshot before re-raising the exception.
               """
        driver = setup
        try:
            # Initialize Home Page object and navigate to URL
            homepage = Home_Page(driver)
            homepage.navigate_to_url()
            logger.info("Navigated to GUVI homepage URL.")

            # Fetch current URL after navigation
            current_url = driver.current_url
            assert current_url == get_config("guvi", "url"), "URL mismatch,Page not loaded successfully"
            logger.info(f"GUVI URL loaded successfully: {current_url}")

            # Capture screenshot on success
            driver.save_screenshot(r"screenshots/TC1_Verify_url.png")
            logger.info("Screenshot captured: TC1_Verify_url.png")

        except AssertionError as ae:
            # Log assertion failures
            logger.error(f"Assertion failed: {ae}")
            driver.save_screenshot(r"screenshots/TC1_Verify_url_Failed.png")
            raise

        except Exception as e:
            # Log any unexpected errors
            logger.exception(f"Unexpected error occurred during URL verification: {e}")
            driver.save_screenshot(r"screenshots/TC1_Verify_url_Error.png")
            raise


    def test_tc2_validate_title(self, setup):
        """
            Test Case 2 : Verify the title of the GUVI homepage

            This test navigates to the GUVI homepage, retrieves the current
            page title, and verifies it matches the expected title from the config file.
            On success, it logs the actual title and saves a screenshot.
            On failure, it logs the error and saves a screenshot before re-raising the exception.
            """
        driver = setup
        homepage = Home_Page(driver)

        try:
            # Step 1: Navigate or load title from homepage
            homepage.get_title()

            # Step 2: Fetch the current page title from browser
            title = driver.title

            # Step 3: Compare actual title with expected title from config
            assert title == get_config("guvi", "title"), "Title mismatch"

            # Step 4: On success, save screenshot and log success message
            driver.save_screenshot(r"screenshots/TC2_Verify_title.png")
            logger.info(f"Title matched successfully: {title}")

        except AssertionError as ae:
            # Handles assertion failure (e.g. title mismatch)
            logger.error(f"Assertion failed: {ae}")
            driver.save_screenshot(r"screenshots/TC2_Verify_title_Failed.png")
            raise

        except Exception as e:
            # Handles any unexpected error during test execution
            logger.exception(f"Unexpected error occurred during title verification: {e}")
            driver.save_screenshot(r"screenshots/TC2_Verify_title_Error.png")
            raise

    def test_tc8_validate_homepage_menu_items(self, setup):
        """
            Test Case 8:  Verify the visibility and click functionality of homepage menu items

            This test retrieves all the menu items on the GUVI homepage and checks
            whether each menu item is visible and clickable. The method
            `verify_and_click_menu_items()` should return a dictionary with menu item names
            as keys and their test status ("Passed"/"Failed") as values.
            The test will assert that all menu items have status "Passed".
            """

        driver = setup
        homepage = Home_Page(driver)

        try:
            # Step 1: Call the page object method to verify menu items
            #         It returns a dict like {"Courses": "Passed", "Login": "Passed", ...}
            results = homepage.verify_and_click_menu_items()

            # Step 2: Loop through each menu item result and assert its status is "Passed"
            for name, status in results.items():
                assert status == "Passed", f"{name} menu test failed: {status}"

            # Step 3: If all assertions passed, capture screenshot for proof
            driver.save_screenshot(r"screenshots/TC8_Verify_menu_items.png")

            # Step 4: Log success if all menu items were verified successfully
            logger.info("All homepage menu items are visible and clickable")

        except AssertionError as ae:
            # Handles assertion failures (if any menu item fails the test)
            logger.error(f"Assertion failed while verifying menu items: {ae}")
            driver.save_screenshot(r"screenshots/TC8_Verify_menu_items_Failed.png")
            raise

        except Exception as e:
            # Handles any unexpected error that occurs during execution
            logger.exception(f"Unexpected error occurred while verifying menu items: {e}")
            driver.save_screenshot(r"screenshots/TC8_Verify_menu_items_Error.png")
            raise

    def test_tc9_validate_dobby_assistant(self, setup):
        """
            Test Case 9 : Verify Dobby Virtual Assistant on GUVI homepage
            Steps:
            1. Verify that the Dobby assistant icon is visible and enabled on the homepage.
            2. Click the Dobby assistant and verify the chatbox title matches the expected value.
            3. Capture a screenshot on success.
            """
        driver = setup
        homepage = Home_Page(driver)
        try:

            # Check if the Dobby bot icon is present and visible
            dobby = homepage.verify_dobby_virtual_assistant()

            assert dobby.is_displayed() and dobby.is_enabled(), \
                "Dobby assistant not displayed or enabled"
            logger.info("Dobby assistant is visible on the homepage")

            # Step 2: Click the Dobby bot icon and fetch the chatbox title
            actual_title = homepage.click_dobby_virtual_assistant()
            expected_title = get_config("guvi", "dobby_title")

            # Step 3: Validate the title of the opened chatbox
            assert actual_title == expected_title, \
                f"Chatbox title mismatch: expected '{expected_title}', got '{actual_title}'"
            logger.info("Dobby assistant chatbox title matched successfully")

            # Step 4: Capture screenshot on successful test execution
            driver.save_screenshot(r"screenshots/TC9_Verify_dobby.png")
            logger.info("dobby virtual assistant is enabled and displayed successfully")

        except AssertionError as ae:
            # Log assertion errors like visibility or title mismatch
            logger.error(f"Assertion failed : {ae}")
            driver.save_screenshot(r"screenshots/TC9_Verify_dobby_Failed.png")
            raise

        except Exception as e:
            # Log any unexpected runtime errors
            logger.exception(f"Unexpected error occurred during Dobby assistant verification: {e}")
            driver.save_screenshot(r"screenshots/TC9_Verify_dobby_Error.png")
            raise

    def test_tc4_validate_signup_button_functionality(self, setup):
        """
            Test Case: TC4 - Validate the functionality of the 'Sign Up' button on the homepage.
            Steps:
            1. Verify that the Sign Up button is displayed and enabled.
            2. Click the Sign Up button and check if the user is navigated to the correct Sign Up page.
            3. Capture a screenshot if the test passes, or on failure.
            """
        driver = setup
        homepage = Home_Page(driver)

        try:
            logger.info("Validate Sign Up button functionality")

            # Step 1: Get the Sign Up button element from the homepage
            signup_button = homepage.get_signup_button()

            # Step 2: Verify the Sign Up button is both visible and enabled and prints result
            assert signup_button.is_displayed() and signup_button.is_enabled(), \
                "signup button not displayed and enabled"
            logger.info("signup button is displayed and enabled")
            print('signup button displayed:', signup_button.is_displayed())
            print('signup button Enabled:', signup_button.is_enabled())

            # Step 3: Click on the Sign Up button
            homepage.click_signup_button()

            # Step 4: Verify if the current URL matches the expected Sign Up page URL
            current_url = driver.current_url
            expected_url = get_config("signup_guvi", "url")
            assert current_url == expected_url, \
                f"URL mismatch: expected '{expected_url}', got '{current_url}'"
            logger.info("Navigated to Sign Up page successfully")

            # Step 5: Take screenshot if all validations passed
            driver.save_screenshot("screenshots/TC4_Verify_signup.png")
            logger.info(r"TC4_Verify_signup_button_functionality executed successfully")

        except AssertionError as ae:
            # Log any assertion failures like button not enabled or URL mismatch
            logger.error(f"Assertion failed : {ae}")
            driver.save_screenshot(r"screenshots/TC4_Verify_signup_Failed.png")
            raise

        except Exception as e:
            # Log any unexpected errors during execution
            logger.exception(f"Unexpected error occurred during Sign Up button verification: {e}")
            driver.save_screenshot(r"screenshots/TC4_Verify_signup_Error.png")
            raise

    def test_tc5_validate_signin_via_signup_functionality(self, setup):
        """
            Test Case 5: Sign In via Sign Up Flow
            Steps:
            1. Fill out the sign-up form with valid user details.
            2. Submit the form and verify successful registration.
            3. Navigate back to homepage and click the Sign Up button again.
            4. From the Sign Up page, click on the 'Login' link to navigate to the login page.
            5. Validate navigation URLs at each step and capture screenshots.
            """
        driver = setup
        homepage = Home_Page(driver)

        try:
            logger.info("Sign In via Sign Up flow")

            # Step 1: Initialize the Signup Page object
            signup=Signup_Page(driver)

            # Step 2: Enter all required sign-up details from config.ini
            signup.enter_name(get_config("signup_guvi", "name"))
            signup.enter_email(get_config("signup_guvi", "email"))
            signup.enter_password(get_config("signup_guvi", "password"))
            signup.enter_mobile_number(get_config("signup_guvi", "mobile"))
            signup.click_signup()

            # Step 3: Fill educational details after initial sign-up
            signup.enter_current_profile_dropdown()
            signup.enter_degree_dropdown()
            signup.enter_year_passed_out(get_config("signup_guvi", "year"))
            signup.click_submit()

            # Step 4: Validate success message is displayed
            success=signup.signup_success_message()
            assert success.is_displayed(),"signup not completed"
            logger.info("Sign up completed successfully")

            # Step 5: Validate current URL after signup
            assert driver.current_url==get_config("signup_guvi","url"),"URL mismatch after signup"

            # Step 6: Navigate back to homepage
            driver.back()

            # Step 7: Click 'Sign Up' button on homepage again
            homepage.click_signup_button()


            # Step 8: Click 'Login' link from the signup page
            signup.click_login_signup_page()

            # Step 9: Validate that user is navigated to the Login page
            assert driver.current_url == get_config("login_guvi", "url"), "URL mismatch after clicking Login"
            logger.info("Navigated from Sign Up to Login page successfully")

            # Step 10: Capture screenshot if everything passed
            driver.save_screenshot(r"screenshots/TC5_Verify_signup.png")
            logger.info("Sign In via Sign Up flow executed successfully")

        except AssertionError as ae:
            # Log assertion errors (field not visible, URL mismatch, etc.)
            logger.error(f"Assertion failed: {ae}")
            driver.save_screenshot(r"screenshots/TC5_Verify_signup_Failed.png")
            raise

        except Exception as e:
            # Log unexpected runtime errors
            logger.exception(f"Unexpected error occurred during Sign Up flow : {e}")
            driver.save_screenshot(r"screenshots/TC5_Verify_signup_Error.png")
            raise



    def test_tc3_validate_login_button_functionality(self, setup):
        """
            Test Case 3: Validate Login Button Functionality
            Steps:
            1. Verify that the Login button on the homepage is displayed and enabled.
            2. Click on the Login button.
            3. Validate navigation to the Login page by comparing the URL from config.
            4. Capture a screenshot and log the result.
            """
        driver = setup
        homepage = Home_Page(driver)

        try:
            logger.info("Validate Login button functionality")

            # Step 1: Get the Login button element from homepage
            login_button = homepage.get_login_button()

            # Step 2: Check if login button is displayed and enabled
            assert login_button.is_displayed() and login_button.is_enabled(), \
                "Login button is not displayed or not enabled"
            logger.info("Login button is displayed and enabled")
            print('Login button displayed:', login_button.is_displayed())
            print('Login button enabled:', login_button.is_enabled())

            # Step 3: Click on the Login button
            homepage.click_login_button()

            # Step 4: Verify that the current URL matches the expected login page URL
            current_url = driver.current_url
            assert current_url == get_config("login_guvi", "url"), \
                "URL mismatch, page not loaded successfully"
            logger.info(f"Login page loaded successfully with URL: {current_url}")

            # Step 5: Capture screenshot if test passed
            driver.save_screenshot(r"screenshots/TC3_Verify_login.png")
            logger.info("login button validation executed successfully")

        except AssertionError as ae:
            # Log assertion errors (like button not visible or wrong URL)
            logger.error(f"Assertion failed : {ae}")
            driver.save_screenshot(r"screenshots/TC3_Verify_login_Failed.png")
            raise

        except Exception as e:
            # Log unexpected runtime errors
            logger.exception(f"Unexpected error occurred : {e}")
            driver.save_screenshot(r"screenshots/TC3_Verify_login_Error.png")
            raise


    @pytest.mark.parametrize(
        "username,password,expected_error",
        [
            # Wrong email with valid password
            (get_config("login_guvi", "invalid_username"), get_config("login_guvi", "valid_password"),
             "Incorrect Email or Password"),
            # Valid email with wrong password
            (get_config("login_guvi", "valid_username"), get_config("login_guvi", "invalid_password"),
             "Incorrect Email or Password")
        ]
    )
    def test_tc7_validate_login_invalid_credentials(self, setup, username, password, expected_error):
        """
            Test Case 7: Validate Login Functionality with Invalid Credentials
            Steps:
            1. Navigate to the Login page.
            2. Enter invalid username/password combinations.
            3. Click the Login button.
            4. Verify that the correct error message is displayed.
            5. Verify that user is not navigated to the dashboard.
            6. Capture a screenshot and log results.
            """

        driver = setup
        loginpage = Login_Page(driver)
        try:
            logger.info(f"StartingTesting login with invalid credentials -> Username: {username}")

            # Step 1: Navigate to the Login page
            loginpage.navigate_to_url()

            # Step 2: Enter username and password
            loginpage.enter_username(username)
            loginpage.enter_password(password)

            # Step 3: Click on the login button
            loginpage.click_login()

            # Step 4: Validate the error message shown
            error_message = loginpage.get_error_message()
            assert error_message == expected_error, \
                f"Expected error '{expected_error}' but got '{error_message}'"
            logger.info(f"Error message validated successfully: {error_message}")

            # Step 5: Ensure user is not redirected to dashboard
            current_url = driver.current_url
            assert current_url != get_config("dashboard_guvi", "url"), \
                "Unexpected navigation to dashboard page"
            logger.info("User not redirected to dashboard as expected")

            # Step 6: Capture screenshot if test passed
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            driver.save_screenshot(f"screenshots/TC7_invalid_login_{timestamp}.png")
            logger.info("invalid log in tested successfully")

        except AssertionError as ae:
            # Log assertion errors like wrong error text or incorrect navigation
            logger.error(f"Assertion failed: {ae}")
            driver.save_screenshot("screenshots/TC7_invalid_credentials_Failed.png")
            raise

        except Exception as e:
            # Log unexpected runtime errors
            logger.exception(f"Unexpected error occurred: {e}")
            driver.save_screenshot("screenshots/TC7_invalid_credentials_Error.png")
            raise


    def test_tc6_validate_login_valid_credentials(self, setup):

        """
            Test Case 6:  Validate Login with Valid Credentials
            Steps:
            1. Navigate to the login page.
            2. Enter valid username and password.
            3. Click the login button.
            4. Wait until the dashboard page loads.
            5. Verify user is redirected to the dashboard.
            6. Capture a screenshot and log results.
            """
        driver = setup
        loginpage = Login_Page(driver)

        try:
            logger.info("Validate login with valid credentials")

            # Step 1: Navigate to login page
            loginpage.navigate_to_url()

            # Step 2: Enter valid username and password from config
            loginpage.enter_username(get_config("login_guvi", "valid_username"))
            loginpage.enter_password(get_config("login_guvi", "valid_password"))

            # Step 3: Click on login button
            loginpage.click_login()

            # Step 4: Wait until the dashboard loads (url contains 'courses')
            loginpage.wait_login_load()

            # Step 5: Verify if user landed on the dashboard page
            current_url = driver.current_url
            expected_url=get_config("dashboard_guvi", "url")
            assert current_url == expected_url, \
                "URL mismatch, Page not loaded successfully"
            logger.info(f"Login successful, user redirected to dashboard page: {expected_url}")

            # Step 6: Capture screenshot on success
            driver.save_screenshot("screenshots/TC6_Verify_Valid_credentials.png")
            logger.info("Valid login credentials executed successfully")

        except AssertionError as ae:
            # Log assertion failures like URL mismatch
            logger.error(f"Assertion failed: {ae}")
            driver.save_screenshot("screenshots/TC6_Verify_Valid_credentials_Failed.png")
            raise

        except Exception as e:
            # Log unexpected runtime errors
            logger.exception(f"Unexpected error occurred: {e}")
            driver.save_screenshot("screenshots/TC6_Verify_Valid_credentials_Error.png")
            raise


    def test_tc10_validate_logout_functionality(self, setup):
        """
            Test Case 10: Validate Logout Functionality
            Steps:
            1. From the dashboard, click the logout dropdown.
            2. Click on the logout option.
            3. Wait until redirected to the homepage.
            4. Validate the user is redirected to the GUVI home page.
            5. Capture a screenshot and log results.
            """
        driver = setup
        logout = Dashboard_Page(driver)

        try:
            logger.info("Validate logout functionality")

            # Step 1: Click the user profile/logout dropdown
            logout.click_logout_dropdown()
            logger.info("Clicked on logout dropdown")

            # Step 2: Click the logout button
            logout.click_logout()
            logger.info("Clicked on logout button")

            # Step 3: Wait until the home page loads after logout
            logout.wait_logout_load()
            logger.info("Waiting for logout to complete")

            # Step 4: Verify user is redirected to GUVI home page after logout
            current_url = driver.current_url
            expected_url= get_config("guvi", "url")
            assert current_url == expected_url, \
                "URL mismatch, Page not loaded successfully after logout"
            logger.info(f"Logout successful, user redirected to GUVI homepage :{expected_url}")

            # Step 5: Capture screenshot on successful logout
            driver.save_screenshot("screenshots/TC10_Verify_logout.png")
            logger.info("account logout validation executed successfully")

        except AssertionError as ae:
            # Log assertion failures like URL mismatch
            logger.error(f"Assertion failed: {ae}")
            driver.save_screenshot("screenshots/TC10_Verify_logout_Failed.png")
            raise

        except Exception as e:
            # Log any unexpected runtime errors
            logger.exception(f"Unexpected error occurred : {e}")
            driver.save_screenshot("screenshots/TC10_Verify_logout_Error.png")

            raise
