# -*- coding: utf-8 -*-

# https://selenium.dev/documentation/en/webdriver/driver_requirements/#firefox
# Simple assignment
import os
import sys
from selenium import webdriver
import mylib
from pyvirtualdisplay import Display
import platform

script_dir = os.path.dirname(os.path.abspath(__file__))

display = None
if platform.system() == 'Linux':
    display = Display(visible=0, size=(800, 600))
    display.start()

ffprofile = webdriver.FirefoxProfile(mylib.get_ffprofile_path("default"))
driver = webdriver.Firefox(executable_path=os.path.join(
    script_dir, "driver", mylib.get_ffdriver_filename()), firefox_profile=ffprofile)

url="https://www.yahoo.co.jp"
if len(sys.argv) == 2:
    url = sys.argv[1]

driver.get(url)
driver.save_screenshot("ss_checkFirefoxDriver.png")

driver.close()
driver.quit()

if display:
    display.stop()
