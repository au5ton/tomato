#!/usr/bin/env python3
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import argparse
import os
import os.path
import re
from time import sleep
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
import platform
IS_MACOS = platform.system() == 'Darwin' # Define boolean for if the platform is macOS or not, useful for Keys.COMMAND vs Keys.CONTROl

PROJECT_DIRECTORY = os.path.split(os.path.realpath(__file__))[0]

# selenium stuff
options = webdriver.ChromeOptions()
# uncomment to maintain cookies between sessions
#options.add_argument("user-data-dir=" + os.environ["CHROME_USER_DATA_DIR"]) # use already logged in user
options.add_argument('--log-level=3')
options.add_argument('--disable-logging')

print("Starting Chrome")
browser = webdriver.Chrome(executable_path=os.environ["CHROMEDRIVER_LOCATION"], chrome_options=options)
browser.get("https://www.tempmailaddress.com/")

temp_email = browser.find_element_by_id("email").text
print("temp email: "+temp_email)

browser.execute_script("window.open('');")
browser.implicitly_wait(2)
browser.switch_to.window(browser.window_handles[1])
browser.get(os.environ["ARCADE_HOMEPAGE"]) # opens other tab to arcade homepage
browser.implicitly_wait(5)

form_element = browser.find_element_by_name("footerEmailForm")
form_input_element = browser.find_element_by_name("footerInputEmai1") 
form_submit_button = browser.find_element_by_css_selector("form[name=\"footerEmailForm\"] input[type=\"submit\"]")
browser.execute_script("arguments[0].scrollIntoView();", form_input_element)
form_input_element.send_keys(temp_email)
form_submit_button.click()
sleep(5)


# # Scroll to and make <input> element visible
# form_element = browser.find_element_by_name("footerEmailForm")
# form_input_element = browser.find_element_by_name("footerInputEmai1")
# browser.execute_script("arguments[0].scrollIntoView();", form_input_element)

# # ready to subscribe, but first we need a new email
# # to create a new email, we need to make a new tab:
# # https://python-forum.io/Thread-Need-Help-Opening-A-New-Tab-in-Selenium

# # Open a new window
# # This does not change focus to the new window for the driver.
# browser.execute_script("window.open('');")
# sleep(0.5)
# # Switch to the new window
# browser.switch_to.window(browser.window_handles[1])
# browser.get("https://www.tempmailaddress.com/")
# sleep(3)
# # close the active tab
# browser.close()
# sleep(3)
# # Switch back to the first tab
# browser.switch_to.window(browser.window_handles[0])
# sleep(3)
# # Close the only tab, will also close the browser.

browser.close()

