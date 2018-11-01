#!/usr/bin/env python3
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import argparse
import os
import os.path
import re
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

PROJECT_DIRECTORY = os.path.split(os.path.realpath(__file__))[0]

# selenium stuff
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=" + os.environ["CHROME_USER_DATA_DIR"]) # use already logged in user
options.add_argument('--log-level=3')
options.add_argument('--disable-logging')

print("Starting Chrome")
driver = webdriver.Chrome(executable_path=os.environ["CHROMEDRIVER_LOCATION"], chrome_options=options)
driver.get("http://www.python.org")
sleep(5)
driver.close()

