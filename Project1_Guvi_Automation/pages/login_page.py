from selenium.webdriver.common.by import By
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (NoSuchElementException,TimeoutException)
from Project1_Guvi_Automation.config_reader import get_config
from Project1_Guvi_Automation.pages.home_page import Home_Page

# Set up logger for this module
logger = logging.getLogger(__name__)

class Login_Page(Home_Page):
    """
        Page Object for the Login Page.
        Provides methods to interact with login fields, submit login form,
        and capture any error messages.
        """
    def __init__(self,driver):
        """
                Initialize the login page with driver and wait.
                Load the login URL from configuration file.
                """
        self.wait = WebDriverWait(driver, 10)
        super().__init__(driver)

        # Load from config.ini
        self.url = get_config("login_guvi", "url")

        # Locators for login elements
        self.username_input=(By.ID, 'email')
        self.password_input=(By.ID, 'password')
        self.login_button=(By.LINK_TEXT, "Login")

        # Locators for possible error messages
        self.incorrect_email_error_message=(By.XPATH,"(//div[text()='Incorrect Email or Password'])[1]")
        self.incorrect_password_error_message = (By.XPATH, "(//div[text()='Incorrect Email or Password'])[2]")


    # --------LOGIN ACTIONS-----------------------

    def enter_username(self,username):
        """ Enter the provided username/email into the username field. """
        try:
            # Wait until username field is visible, then send keys
            self.wait.until(EC.visibility_of_element_located(self.username_input)).send_keys(username)
            logger.info(f"Entered username: {username}")

        except (NoSuchElementException, TimeoutException) as e:
            logger.error(f"Username/email field not found: {e}")
            raise AssertionError(f"Username/email field not found: {e}")


    def enter_password(self,password):
        """ Enter the provided password into the password field."""
        try:
            # Wait until password field is visible, then send keys
            self.wait.until(EC.visibility_of_element_located(self.password_input)).send_keys(password)
            logger.info("Entered password on Login page")

        except (NoSuchElementException, TimeoutException) as e:
            logger.error(f"Password field not found: {e}")
            raise AssertionError(f"Password field not found: {e}")

    #  ---- SUBMIT BUTTON------

    def click_login(self):
        """ Click on the Login button to submit the login form."""
        try:
            # Wait until login button is clickable, then click
            self.wait.until(EC.element_to_be_clickable(self.login_button)).click()
            logger.info("Login button clicked successfully")

        except TimeoutException as e:
            logger.error(f"Login button not found/clickable: {e}")
            raise AssertionError(f"Login button not found: {e}")


    def wait_login_load(self):
        """ Wait for the login to complete and the URL to contain 'courses'."""
        try:
            # Wait until the page URL contains 'courses' indicating successful login
            self.wait.until(EC.url_contains("courses"))
            logger.info("Login successful, navigated to user Home page.")

        except TimeoutException as e:
            logger.error(f"Login did not redirect to courses page: {e}")
            raise AssertionError(f"Login not successful: {e}")


    def get_error_message(self):
        """Return whichever error is visible. Checks for both email and password errors."""
        errors = [
            self.incorrect_email_error_message,
            self.incorrect_password_error_message,
        ]

        # Check each possible error locator
        for error_locator in errors:
            try:
                # Wait until element is visible and get its text
                error = self.wait.until(EC.visibility_of_element_located(error_locator))
                text = error.text
                if text and text.strip():
                    logger.info(f"Login error message displayed: {text.strip()}")
                    return text.strip()

            except Exception:
                # If not found, move to next locator
                continue


            # If no error is visible, return None
        logger.info("No error message displayed on login")
        return None




