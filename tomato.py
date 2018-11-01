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
browser.get(os.environ["ARCADE_HOMEPAGE"])
sleep(1) # wait for page to load

# Scroll to and make <input> element visible
form_element = browser.find_element_by_name("footerEmailForm")
form_input_element = browser.find_element_by_name("footerInputEmai1")
browser.execute_script("arguments[0].scrollIntoView();", form_input_element)

# ready to subscribe, but first we need a new email
# to create a new email, we need to make a new tab:
# https://gist.github.com/lrhache/7686903

# create clickable link to where we want to go
browser.execute_script("var link = document.createElement(\'a\'); link.href = \'https://www.tempmailaddress.com\'; link.innerText = \'tomato\'; link.id = \'tomato_link\'; document.body.appendChild(link);")
first_link = browser.find_element_by_id('tomato_link')

# Save the window opener (current window, do not mistaken with tab... not the same)
main_window = browser.current_window_handle
first_link.send_keys(Keys.CONTROL + Keys.RETURN)

# Switch tab to the new tab, which we will assume is the next one on the right
browser.find_element_by_tag_name('body').send_keys((Keys.COMMAND if IS_MACOS else Keys.CONTROL) + Keys.TAB)
    
# Put focus on current window which will, in fact, put focus on the current visible tab
browser.switch_to_window(main_window)

# do whatever you have to do on this page, we will just got to sleep for now
sleep(2)

# Close current tab
browser.find_element_by_tag_name('body').send_keys((Keys.COMMAND if IS_MACOS else Keys.CONTROL) + 'w')

# Put focus on current window which will be the window opener
browser.switch_to_window(main_window)

form_input_element.send_keys("some text")
sleep(3)


browser.close()

