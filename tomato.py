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

PROJECT_DIRECTORY = os.path.split(os.path.realpath(__file__))[0]

# selenium stuff
options = webdriver.ChromeOptions()
# uncomment to maintain cookies between sessions
#options.add_argument("user-data-dir=" + os.environ["CHROME_USER_DATA_DIR"]) # use already logged in user
options.add_argument('--log-level=3')
options.add_argument('--disable-logging')

print("Starting Chrome")
driver = webdriver.Chrome(executable_path=os.environ["CHROMEDRIVER_LOCATION"], chrome_options=options)
driver.get(os.environ["ARCADE_HOMEPAGE"])
sleep(1) # wait for page to load

# Scroll to and make <input> element visible
form_element = driver.find_element_by_name("footerEmailForm")
form_input_element = driver.find_element_by_name("footerInputEmai1")
driver.execute_script("arguments[0].scrollIntoView();", form_input_element)

# ready to subscribe, but first we need a new email
# to create a new email, we need to make a new tab:
# https://gist.github.com/lrhache/7686903

# create clickable link to where we want to go
driver.execute_script("var link = document.createElement(\'a\'); link.href = \'https://www.tempmailaddress.com\'; link.innerText = \'tomato\'; link.id = \'tomato_link\'; document.body.appendChild(link);")

# Save the window opener (current window, do not mistaken with tab... not the same)
main_window = browser.current_window_handle


form_input_element.send_keys("some text")
sleep(3)


driver.close()

