#!/usr/bin/env python3
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import requests
import os
import os.path
import re
import argparse
from time import sleep
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
import platform
IS_MACOS = platform.system() == 'Darwin' # Define boolean for if the platform is macOS or not, useful for Keys.COMMAND vs Keys.CONTROl

PROJECT_DIRECTORY = os.path.split(os.path.realpath(__file__))[0]

def do_automation():

    # selenium stuff
    options = webdriver.ChromeOptions()
    # uncomment to maintain cookies between sessions
    #options.add_argument("user-data-dir=" + os.environ["CHROME_USER_DATA_DIR"]) # use already logged in user
    options.add_argument('--log-level=3')
    options.add_argument('--disable-logging')

    print("\tStarted Chrome")
    browser = webdriver.Chrome(executable_path=os.environ["CHROMEDRIVER_LOCATION"], chrome_options=options)
    browser.get("https://www.tempmailaddress.com/")

    temp_email = browser.find_element_by_id("email").text
    print("\ttemp email: "+temp_email)

    # opens and loads new arcade homepage
    print("\tOpening Arcade homepage")
    browser.execute_script("window.open('');")
    browser.implicitly_wait(2)
    browser.switch_to.window(browser.window_handles[1])
    browser.get(os.environ["ARCADE_HOMEPAGE"])
    browser.implicitly_wait(5)

    # subscribes user on arcade homepage
    print("\tSubscribing temp email")
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
    sleep(5)
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
    print("\tInjecting MEFormFiller javascript")
    browser.execute_script(open("./MEFormFiller.user.js").read())
    browser.implicitly_wait(5)
    sleep(5)
    iframe2 = browser.find_element_by_css_selector('iframe#MarketingMicrositeIfr')
    browser.switch_to_frame(iframe2)
    browser.find_element_by_css_selector("button[name='ME_TabbedScreenFlow7_pyWorkPage_15']").click()
    sleep(5)
    browser.find_element_by_css_selector("button[name='ME_TabbedScreenFlow7_pyWorkPage_16']").click()
    sleep(5)
    browser.close()
    browser.switch_to.window(browser.window_handles[0])
    sleep(5)

    # back to email to claim QR code
    browser.switch_to_default_content()
    sleep(5)
    browser.find_element_by_css_selector("span.glyphicon-share-alt").click()
    browser.implicitly_wait(5)
    browser.find_element_by_css_selector("#schranka tr[data-href='3'].hidden-xs").click() # opens 3rd email received, gift receipt
    browser.implicitly_wait(5)

    # open individual email
    iframe3 = browser.find_element_by_id('iframeMail')
    browser.switch_to_frame(iframe3)
    qr_code = browser.find_element_by_css_selector("img.cursordefault").get_attribute("src")
    print("\tQR code: "+qr_code)
    r = requests.get(qr_code, allow_redirects=True)
    open(os.path.basename(qr_code), 'wb').write(r.content)
    print("Saved to: "+os.path.basename(qr_code))
    browser.switch_to_default_content()
    browser.close()

    return

# cli arguments
parser = argparse.ArgumentParser()
parser.add_argument("-L", action="store", dest="count", default="3", help="Specify card count as an integer")
args = parser.parse_args()

if args.count is None:
    print("Must specify count with -L, see --help")
    exit(1)

for i in range(1,int(args.count)+1):
    print("Card [{}/{}]:".format(str(i), str(int(args.count))))
    do_automation()