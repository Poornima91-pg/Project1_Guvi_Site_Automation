import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.edge.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from Project1_Guvi_Automation.config_reader import get_config # <-- To read browser from config.ini
import logging

# Configure logging inside setup
logger = logging.getLogger(__name__)

def pytest_addoption(parser):
    """
    Pytest hook to add a command-line option for browser name.
    This allows passing --browser-name at runtime.
    """
    parser.addoption(
        "--browser-name",default = 'chrome', help="This will take browser name from user"
    )

@pytest.fixture(scope='class') # set up and tear down
def setup(request):
    """
    Pytest fixture to set up and tear down the Selenium WebDriver.

    Steps:
    1. Read browser name from command line or config.ini
    2. Launch the respective browser using WebDriverManager
    3. Maximize window and set implicit wait
    4. Return driver instance to the test
    5. Quit driver after test completes
    """
    driver = None
    try:
        # Get browser from Command line first, else from config file
        browser_name = request.config.getoption("--browser-name") or get_config("browser_name", "browser")
        logger.info(f"Selected browser: {browser_name}")
        browser = browser_name.lower()

        # Initialize the driver based on browser name
        if browser == 'chrome':
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            logger.info("Launched Chrome browser")

        elif browser == 'firefox':
            driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
            logger.info("Launched Firefox browser")

        elif browser == 'edge':
            driver = webdriver.Edge()
            logger.info("Launched Edge browser")

        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

        # Browser window setup
        driver.maximize_window()
        driver.implicitly_wait(10)

        # Attach the driver to the class so page objects can access it
        request.cls.driver = driver

        # Yield to test, then teardown
        yield driver

    except Exception as e:
        # Log unexpected errors during setup
        logger.exception(f"Error occurred while launching browser: {e}")
        raise

    finally:
        # Quit the browser after test completion
        if driver:
            logging.info("Closing the browser")
            driver.quit()


def pytest_configure():
    """
    Pytest to configure logging before tests start.
    Configure the root logger to log INFO and above level messages to both file and console.
    Sets up both file and console handlers with a common formatter.
    """
    try:
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

        # File handler for saving logs to file
        file_handler = logging.FileHandler("test_logs.log")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Console handler to print logs on terminal
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        logger.info("Logging configured successfully")

    except Exception as e:
        print(f"Failed to configure logging: {e}")