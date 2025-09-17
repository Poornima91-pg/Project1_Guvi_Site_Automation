from selenium.webdriver.common.by import By
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (NoSuchElementException,TimeoutException)
from Project1_Guvi_Automation.config_reader import get_config
from Project1_Guvi_Automation.pages.home_page import Home_Page

# Set up logger for this module
logger = logging.getLogger(__name__)

class Dashboard_Page(Home_Page):
    """
        Page Object for the Dashboard Page.
        Inherits from Home_Page and contains actions specific to the dashboard.
        """
    def __init__(self,driver):
        """Initialize dashboard Page elements and load configuration values."""

        # Create WebDriverWait instance for waiting on elements
        self.wait = WebDriverWait(driver, 30)
        # Call parent constructor to initialize driver
        super().__init__(driver)

        # Load expected dashboard page title from config.ini
        self.url = get_config("dashboard_guvi", "url")

        # Locators for logout elements
        # Profile dropdown menu
        self.logout_dropdown=(By.ID,"dropdown_contents")
        # Logout option inside dropdown
        self.logout_button=(By.XPATH,"(//div[@id='dropdown_contents'])[3]")

   # ----------------- LOGOUT ACTION------------------------

    def click_logout_dropdown(self):
        """ Click on the profile dropdown to open it. """
        try:
            # Wait until dropdown is clickable and click
            self.wait.until(EC.element_to_be_clickable(self.logout_dropdown)).click()
            logger.info("Clicked on logout dropdown successfully.")

        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Failed to click logout dropdown: {e}")
            raise AssertionError(f"Logout dropdown not clickable: {e}")

    def click_logout(self):
        """ Click the logout button from the dropdown."""
        try:
            # Wait until logout button is clickable and click
            self.wait.until(EC.element_to_be_clickable(self.logout_button)).click()
            logger.info("Clicked on logout button successfully.")

        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Logout button click failed: {e}")
            raise AssertionError(f"Logout process failed: {e}")

    def wait_logout_load(self):
        """
              Wait until the page redirects back to the login/home page after logout.
              """
        try:
            # Wait until URL is the expected homepage URL after logout
            self.wait.until(EC.url_to_be(get_config("guvi", "url")))
            logger.info("Logout successful, redirected to homepage.")

        except TimeoutException as e:
            logger.error(f"Did not return to homepage after logout: {e}")
            raise AssertionError(f"Login button not found after logout: {e}")