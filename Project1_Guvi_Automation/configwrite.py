from configparser import ConfigParser

"""
create_config.py

This module generates a configuration file (config.ini) for automating tests on the GUVI web application.
It stores test data and environment details like browser name, URLs, login credentials, and expected titles.
The config file is used throughout the automation framework to achieve maintainability and reusability.
"""

def create_config():
    """
        Creates a configuration file 'config.ini' with sections for:
        - browser configuration
        - application URLs
        - login credentials
        - signup details
        - dashboard details
        """

    # Create a ConfigParser object to write config data
    config = ConfigParser()

    # Browser configuration
    config["browser_name"]= {
        # browser options: chrome, firefox, edge
        "browser":"chrome"
    }

    # GUVI homepage details
    config["guvi"] = {
        "url": "https://www.guvi.in/",
        "title": "GUVI | Learn to code in your native language",
        "dobby_title":"Dobby",
        "course_url":"https://www.guvi.in/courses/?current_tab=paidcourse"
    }

    # Login page details and test credentials
    config["login_guvi"]={
        "url": "https://www.guvi.in/sign-in/",
        "valid_username":"Ganesh1824@gmail.com",
        "valid_password":"Abcd@123",
        "invalid_username": "Ganesh24@gmail.com",
        "invalid_password": "Ab@123"
    }

    # Signup page details and dummy user data
    config["signup_guvi"] = {
        "url": "https://www.guvi.in/register/",
        "name": "Poornima",
        "email": "guvi129001@gmail.com",
        "password": "Abcd@1234",
        "mobile": "1234567890",
        "year":"2012"
    }

    # Dashboard URL details
    config["dashboard_guvi"]={
        "url": "https://www.guvi.in/courses/?current_tab=myCourses"
    }

    # Write the configuration data to config.ini file
    with open("config.ini", "w") as configfile:
        config.write(configfile)

if __name__ == "__main__":
    create_config()



