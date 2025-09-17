from selenium.webdriver.common.by import By
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (NoSuchElementException,TimeoutException)
from Project1_Guvi_Automation.config_reader import get_config

# Create a logger for this module
logger = logging.getLogger(__name__)

class Home_Page():
    def __init__(self,driver):
        """
            Page Object Model (POM) class for the GUVI Home Page.
            It contains:
                - All locators on the homepage
                - Reusable actions (methods) to interact with homepage elements
                - Assertions to verify UI behavior
            """
        # Store driver instance
        self.driver=driver
        # WebDriverWait to use throughout the class (default 30 sec)
        self.wait = WebDriverWait(self.driver, 30)

        # Load config values from config.ini
        self.url = get_config("guvi", "url")
        self.title = get_config("guvi", "title")
        self.dobby_title=get_config("guvi","dobby_title")
        self.course_url=get_config("guvi","course_url")

        # -------Locators------
        # Header buttons
        self.login_button=(By.LINK_TEXT, "Login")
        self.signup_button=(By.XPATH,"//a[text()='Sign up']")

        # Top menu items
        self.Menu_items={
            "Courses":(By.XPATH,"//a[contains(@class,'rwl3jt-0 my-2')]"),
            "Live_class":(By.XPATH,"//p[text()='LIVE Classes']"),
            "Practice":(By.XPATH,"//p[@id='practiceslink']")
        }
        # Dropdown elements for menu items
        self.live_class_dropdown = (By.XPATH, "(//ul[@class='⭐️rwl3jt-0 list-none'])[5]")
        self.practice_dropdown = (By.XPATH, "(//ul[@class='⭐️rwl3jt-0 list-none'])[6]")

        # Dobby virtual assistant elements
        self.iframe_dobby=(By.CSS_SELECTOR, "iframe[title='chat window']")
        self.click_dobby_assistant = (By.ID, 'ym-auto-pop-up-content')
        self.dobby_chatbox = (By.XPATH,"//div[@id='chatContainer']//div[@id='chat-title']")

    # ---------------------- BASIC PAGE ACTIONS ----------------------

    def navigate_to_url(self):
        """Navigate to the homepage URL and wait for it to load."""
        try:
            logger.info(f"Navigating to URL: {self.url}")
            self.driver.get(self.url)
            self.wait.until(EC.url_to_be(self.url))
            logger.info(f"Successfully navigated to: {self.url}")

        except TimeoutException as e:
            logger.error(f"Failed to navigate to {self.url}: {e}")
            raise AssertionError(f"Failed to navigate to URL: {e}")


    def get_title(self):
        """Return the page title after verifying it contains expected text."""
        try:
            logger.info("Waiting for page title to contain 'GUVI | Learn to code'")
            self.wait.until(EC.title_contains("GUVI | Learn to code"))
            logger.info(f"Page title found: {self.driver.title}")
            return self.driver.title

        except TimeoutException as e:
            logger.error(f"Page title did not contain expected text: {e}")
            raise AssertionError(f"Page title verification failed: {e}")

    # ---------------------- LOGIN BUTTON ----------------------

    def get_login_button(self):
        """Locate and return the Login button element."""
        try:
            logger.info("Waiting for Login button to be clickable")
            login=self.wait.until(EC.element_to_be_clickable(self.login_button))
            logger.info("Login button located successfully")
            return login

        except (NoSuchElementException, TimeoutException) as e:
            logger.error(f"Login button not found: {e}")
            raise AssertionError(f"Login button not found: {e}")


    def click_login_button(self):
        """Click the Login button and verify navigation to sign-in page."""
        try:
             logger.info("Attempting to click Login button")
             self.get_login_button().click()
             self.wait.until(EC.url_contains("sign-in"))
             logger.info("Clicked on Login button and navigated to sign-in page")

        except (NoSuchElementException, TimeoutException) as e:
            logger.error(f"Login button click failed: {e}")
            raise AssertionError(f"Login button not found: {e}")


    # ---------------------- SIGNUP BUTTON ----------------------

    def get_signup_button(self):
        """Locate and return the Sign up button element."""
        try:
            logger.info("Waiting for Sign up button to be clickable")
            signup =self.wait.until(EC.element_to_be_clickable(self.signup_button))
            logger.info("Sign up button located successfully")
            return signup

        except (NoSuchElementException, TimeoutException) as e:
            logger.error(f"Sign up button not found: {e}")
            raise AssertionError(f"Sign up button not found: {e}")

    def click_signup_button(self):
        """Click the Sign up button and verify navigation to register page."""
        try:
            logger.info("Attempting to click Sign up button")
            self.get_signup_button().click()
            self.wait.until(EC.url_contains("register"))
            logger.info("Clicked on Sign up button and navigated to register page")

        except (NoSuchElementException, TimeoutException) as e:
            logger.error(f"Sign up button click failed: {e}")
            raise AssertionError(f"Sign up button not found: {e}")


    # ---------------------- MENU ITEMS VERIFICATION ----------------------

    def verify_and_click_menu_items(self):
        """
        Verify top menu items are visible, enabled, and clickable.
        Click on each and validate:
            - Courses should navigate to courses page
            - Live_class should show dropdown
            - Practice should show dropdown
        Returns a dict {menu_name: "Passed"/"Failed: reason"}.
        """
        results = {}

        for name, locator in self.Menu_items.items():
            try:
                # Wait for menu item to be clickable
                logger.info(f"Checking menu item '{name}' is clickable")
                element = self.wait.until(EC.element_to_be_clickable(locator))
                assert element.is_displayed() and element.is_enabled(), f"{name} menu not visible or enabled"
                logger.info(f"Menu '{name}' is visible and enabled")

                # Click the menu item
                element.click()
                logger.info(f"Clicked on '{name}' menu item")

                # Handle each menu item behavior
                if name == "Courses":
                    logger.info("Verifying Courses navigation")
                    self.wait.until(EC.url_to_be(self.course_url))
                    assert self.driver.current_url== self.course_url, f"Clicking '{name}' did not navigate"
                    logger.info("Courses page navigation verified")

                    # Go back to homepage
                    self.driver.back()
                    self.wait.until(EC.url_to_be(get_config("guvi","url")))
                    self.wait.until(EC.element_to_be_clickable(locator))

                elif name == "Live_class":
                    # Verify Live Class dropdown
                    logger.info("Verifying Live Classes dropdown")
                    dropdown = self.wait.until(EC.visibility_of_element_located(self.live_class_dropdown))
                    assert dropdown.is_displayed() and dropdown.is_enabled(), "Live Classes dropdown not visible or enabled"
                    logger.info("Live Classes dropdown is visible and enabled")

                elif name == "Practice":
                    # Verify Practice dropdown
                    logger.info("Verifying Practice dropdown")
                    dropdown = self.wait.until(EC.visibility_of_element_located(self.practice_dropdown))
                    assert dropdown.is_displayed() and dropdown.is_enabled(), "Practice dropdown not visible or enabled"
                    logger.info("Practice dropdown is visible and enabled")

                results[name] = "Passed"


            except (NoSuchElementException, TimeoutException, AssertionError) as e:
                logger.error(f"Menu '{name}' verification failed: {e}")
                results[name] = f"Failed: {e}"

        return results

    # ---------------------- DOBBY VIRTUAL ASSISTANT ----------------------

    def verify_dobby_virtual_assistant(self):
        """
        Verify that the Dobby virtual assistant icon is present on the page.
        Returns the clickable Dobby element.
        """
        try:
            logger.info("Waiting for Dobby assistant icon to be clickable")
            chatbox = self.wait.until(EC.element_to_be_clickable(self.click_dobby_assistant))

            assert chatbox.is_displayed() and chatbox.is_enabled(), \
                "Dobby assistant button is not displayed or not enabled"
            logger.info("Dobby assistant is visible and enabled on the homepage")

            return chatbox
        except (NoSuchElementException, TimeoutException) as e:
            logger.error(f"Dobby assistant not found: {e}")
            raise AssertionError(f"Dobby assistant not found: {e}")

    def click_dobby_virtual_assistant(self):
        """
            Click the Dobby virtual assistant icon,
            switch to its iframe, verify the chatbox appears,
            then switch back to main content.
            """
        try:
            logger.info("Clicking on Dobby assistant icon")
            # Click on the Dobby assistant icon
            self.verify_dobby_virtual_assistant().click()
            logger.info("Clicked on Dobby assistant button")

            # Wait for the iframe to appear
            logger.info("Waiting for Dobby iframe to appear")
            iframe = self.wait.until(EC.presence_of_element_located(self.iframe_dobby))

            # Switch driver context into the iframe
            self.driver.switch_to.frame(iframe)
            logger.info("Switched to Dobby assistant iframe")

            # wait for the chatbox inside iframe
            logger.info("Waiting for Dobby chatbox inside iframe")
            chatbox = self.wait.until(EC.visibility_of_element_located(self.dobby_chatbox))

            # Verify chatbox visibility
            assert chatbox.is_displayed() and chatbox.is_enabled(), \
                "Dobby chatbox is not displayed or not enabled"
            logger.info("Dobby assistant chatbox is fully visible")

            # Get and log chatbox title
            chatbox_title = chatbox.text.strip()
            logger.info(f"Dobby assistant chatbox title: {chatbox_title}")

            # Switch back to the main page
            self.driver.switch_to.default_content()
            logger.info("Switched back to main page")

            return chatbox_title

        except (NoSuchElementException, TimeoutException) as e:
            logger.error(f"Dobby chatbox not found or not loaded: {e}")
            raise AssertionError(f"Dobby chatbox not found: {e}")