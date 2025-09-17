from selenium.webdriver.common.by import By
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (NoSuchElementException,TimeoutException)
from selenium.webdriver.support.select import Select
from Project1_Guvi_Automation.config_reader import get_config
from Project1_Guvi_Automation.pages.home_page import Home_Page

# Configure logger
logger = logging.getLogger(__name__)

class Signup_Page(Home_Page):

    def __init__(self,driver):
        """Initialize Signup Page elements and load configuration values."""

        # Create WebDriverWait instance for waiting on elements
        self.wait = WebDriverWait(driver, 10)

        # Call parent constructor to initialize driver
        super().__init__(driver)

        # Get the signup page URL from config.ini
        self.url = get_config("signup_guvi", "url")

        # Locators for all the elements on the Signup Page
        self.name_input=(By.ID, 'name')
        self.email_input=(By.ID, 'email')
        self.password_input=(By.ID, "password")
        self.mobile_number_input=(By.ID, 'mobileNumber')
        self.signup_button=(By.XPATH,"(//a[text()='Sign Up'])[1]")
        self.current_profile_dropdown=(By.ID,'profileDrpDwn')
        self.degree_dropdown=(By.ID,'degreeDrpDwn')
        self.year_passout_input=(By.ID,'year')
        self.submit_button=(By.ID,'details-btn')
        self.signup_sucess=(By.XPATH,"//div[@class='left-head']//h1[text()='Almost Done! Check Your Inbox!']")
        self.signup_login=(By.CLASS_NAME,"login")

    # ---------- FORM FIELD ACTIONS ----------

    def enter_name(self,name):
        """Enter the full name into the name field."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.name_input)).send_keys(name)
            logger.info(f"Entered username: {name}")

        except (NoSuchElementException, TimeoutException) as e:
            logger.error(f"Failed to enter name: {e}")
            raise AssertionError(f"Name field not found: {e}")

    def enter_email(self, email):
        """Enter the email into the email field."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.email_input)).send_keys(email)
            logger.info(f"Entered email: {email}")

        except (NoSuchElementException, TimeoutException) as e:
            logger.error(f"Failed to enter email: {e}")
            raise AssertionError(f"Email field not found: {e}")

    def enter_password(self, password):
        """Enter the password into the password field."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.password_input)).send_keys(password)
            logger.info(f"Entered password: {password}")

        except (NoSuchElementException, TimeoutException) as e:
            logger.error(f"Failed to enter password: {e}")
            raise AssertionError(f"Password field not found: {e}")

    def enter_mobile_number(self, number):
        """Enter the mobile number into the mobile number field."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.mobile_number_input)).send_keys(number)
            logger.info(f"Entered mobile number: {number}")

        except (NoSuchElementException, TimeoutException) as e:
            logger.error(f"Failed to enter mobile number: {e}")
            raise AssertionError(f"Mobile number field not found: {e}")

    # --------------------- BUTTONS ---------------------

    def click_signup(self):
        """Click the Sign Up button."""
        try:
            self.wait.until(EC.element_to_be_clickable(self.signup_button)).click()
            logger.info("Clicked Sign Up button")

        except TimeoutException as e:
            logger.error(f"Sign Up button not clickable: {e}")
            raise AssertionError(f"Sign Up button not found: {e}")

    # --------------------- DROPDOWNS ---------------------

    def enter_current_profile_dropdown(self):
        """Select 'Looking for a career' from Current Profile dropdown."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.current_profile_dropdown))
            profile=Select(self.driver.find_element(*self.current_profile_dropdown))
            profile.select_by_value('Looking for a career')
            logger.info("Selected Current Profile: Looking for a career")

        except TimeoutException as e:
            logger.error(f"Failed to select Current Profile: {e}")
            raise AssertionError(f"Current Profile dropdown not found: {e}")


    def enter_degree_dropdown(self):
        """Select 'B.E. / B.Tech. Computer Science' from Degree dropdown."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.degree_dropdown))
            degree=Select(self.driver.find_element(*self.degree_dropdown))
            degree.select_by_value('B.E. / B.Tech. Computer Science')
            logger.info("Selected Degree: B.E. / B.Tech. Computer Science")

        except TimeoutException as e:
            logger.error(f"Failed to select Degree: {e}")
            raise AssertionError(f"Degree dropdown not found: {e}")

    # --------------------- OTHER FIELDS ---------------------

    def enter_year_passed_out(self,year):
        """Enter the passing year."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.year_passout_input)).send_keys(year)
            logger.info(f"Entered passing year: {year}")

        except (NoSuchElementException, TimeoutException) as e:
            logger.error(f"Failed to enter passing year: {e}")
            raise AssertionError(f"Year field not found: {e}")

    def click_submit(self):
        """Click the Submit button."""
        try:
            self.wait.until(EC.element_to_be_clickable(self.submit_button)).click()
            logger.info("Clicked Submit button")

        except TimeoutException as e:
            logger.error(f"Submit button not clickable: {e}")
            raise AssertionError(f"Submit button not found: {e}")

    # --------------------- VALIDATIONS ---------------------

    def signup_success_message(self):
        """Verify if signup success message is displayed."""
        try:
            success=self.wait.until(EC.presence_of_element_located(self.signup_sucess))
            assert success.is_displayed,'success message displayed'
            logger.info("Signup success message displayed")
            return success

        except TimeoutException as e:
            logger.error(f"Signup success message not found: {e}")
            raise AssertionError(f"Success message not found: {e}")

    def click_login_signup_page(self):
        """Click the Login link on the signup page and wait for login page to load."""
        try:
            self.wait.until(EC.element_to_be_clickable(self.signup_login)).click()
            self.wait.until(EC.url_contains("sign-in"))
            logger.info("Navigated to Login page from Signup page")

        except TimeoutException as e:
            logger.error(f"Login link not found or page not loaded: {e}")
            raise AssertionError(f"Login link not found: {e}")