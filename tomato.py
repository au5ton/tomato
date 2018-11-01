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

# opens and loads new arcade homepage
browser.execute_script("window.open('');")
browser.implicitly_wait(2)
browser.switch_to.window(browser.window_handles[1])
browser.get(os.environ["ARCADE_HOMEPAGE"])
browser.implicitly_wait(5)

# subscribes user on arcade homepage
form_element = browser.find_element_by_name("footerEmailForm")
form_input_element = browser.find_element_by_name("footerInputEmai1") 
form_submit_button = browser.find_element_by_css_selector("form[name=\"footerEmailForm\"] input[type=\"submit\"]")
browser.execute_script("arguments[0].scrollIntoView();", form_input_element)
form_input_element.send_keys(temp_email)
form_submit_button.click()
sleep(5)
browser.close()

# back to tempmailaddress.com, previous tab
browser.switch_to.window(browser.window_handles[0])
browser.implicitly_wait(5)
browser.find_element_by_css_selector("a[href='#refresh']:not(.btn)").click()
sleep(2)
browser.find_element_by_css_selector("#schranka tr[data-href='2'].hidden-xs").click() # opens 2nd email received, subscription confirmation
browser.implicitly_wait(5)

# open individual email
iframe = browser.find_element_by_id('iframeMail')
browser.switch_to_frame(iframe)
browser.find_element_by_css_selector("a.mktbutton").click() # opens subscription signup
browser.implicitly_wait(5)
sleep(5)

# interact with signup form
browser.switch_to.window(browser.window_handles[1]) # switches to 2nd tab
print(browser.current_url)
browser.execute_script(open("./MEFormFiller.user.js").read())
browser.implicitly_wait(5)
iframe2 = browser.find_element_by_css_selector('iframe#MarketingMicrositeIfr')
browser.switch_to_frame(iframe2)
browser.find_element_by_css_selector("button[name='ME_TabbedScreenFlow7_pyWorkPage_15']").click()
browser.implicitly_wait(5)
browser.find_element_by_css_selector("button[name='ME_TabbedScreenFlow7_pyWorkPage_16']").click()
sleep(5)
browser.close()


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

