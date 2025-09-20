**GUVI-SITE - POM**
Automated Testing of the EdTech Platform Web Application 
Website Link: https://www.guvi.in/

**Test Objective:**
Launching Guvi website and testing start automation —  
The objective of this project is to automate the testing of the web application (https://www.guvi.in) by simulating user actions and 
validating key UI functionalities.  
This includes verifying page behavior, accessibility of critical elements, navigation flows, and login functionalities.

**Guvi Site Automation EdTech Platform Web Application using pytest and Selenium:**
**Project Overview:**
This project is a test automation suite for the Guvi website, developed using **pytest** and **Selenium**.  
The main objective is to automate functional testing for various flows in the application, such as:

- Launching the URL
- Registering a new user
- User authentication (login/logout)
- Homepage UI elements validation

This project is built on the **Page Object Model (POM)** design and ensures that the site operates as expected and offers a seamless experience to users.

**It includes:**
- Page Object Model (POM)
- Data Driven Testing (via `config.ini`)
- Logging using Python `logging` module
- Multi-browser support (Chrome, Firefox, Edge) via `webdriver_manager`
- Test cases for login, signup, logout, and homepage validations

**Table of Contents:**
Features
Tech Stack
Setup and Installation
Running Tests
Project Structure

**Features:**
* Login - valid and invalid credentials
* Signup and redirect to login
* Logout functionality
* Homepage menu item validation
* Dobby assistant chat validation
* Config setup
* Cross-browser support

**Tech Stack**
Programming Language: Python
Test Framework: pytest
Automation Tool: Selenium WebDriver
Reporting: pytest-html
Browser Compatibility: Chrome, Firefox, and Edge

**Setup and Installation**
To set up and run this project locally, follow these steps:

**Install Dependencies:**
pip install -r requirements.txt

**Set Up Environment Variables:**
Create a config.ini file in the project root to store environment data like credentials and browser.
[browser_name]
browser = chrome

[guvi]
url = https://www.guvi.in/

[login_guvi]
valid_username = test@example.com
valid_password = yourpassword
invalid_username = wrong@example.com
invalid_password = wrongpass

[signup_guvi]
url = https://www.guvi.in/register
name = YourName
email = your_email@example.com
password = yourpassword
mobile = 9999999999
year = 2024

**Running Tests**
To execute tests, use the following commands:

**Run All Tests with default browser(chrome) in config.ini file and displayed result on console:**
change to required browser name in configwrite.py file and run it then run the below command
 pytest -v -s 

**Run All Tests with browser passed through command line and displayed result on console:**
 pytest -v --browser-name firefox

**Run All Tests with default browser(chrome) in config.ini file and generate html report**
Generate HTML Report:
pytest --html=report.html -v -s

**Logs & Reports**
Logs are stored in test_logs.log
Reports are stored in report.html
Screenshots for failed/passed tests are saved inside the screenshots/ directory.

**Project Structure**
Guvi-page-automation-pytest-selenium/
├── tests/                                    # All test cases
│   ├── test_guvi_page_automation.py          
├── pages/                                    # Page Object Models for each page
│   ├── home_page.py
│   ├── login_page.py
│   ├── signup_page.py
│   ├── dashboard_page.py
├── screenshots/                              # screenshot location for each testcase
│   ├── test_case_1                        
│   ├── test_case_2             
├── conftest.py                               # browser and logger setup
├── config.ini                                # Environment variables
├── configwrite.py                            # Environment variables writer file
├── config_reader.py                          # Environment variables reader file
├── requirements.txt                          # Project dependencies
├── testlog.log                               # Test log file
└── README.md                                 # Project documentation

