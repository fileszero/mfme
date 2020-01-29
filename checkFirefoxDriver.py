# -*- coding: utf-8 -*-

# https://selenium.dev/documentation/en/webdriver/driver_requirements/#firefox
# Simple assignment
import os
import sys
from selenium import webdriver
import mylib

script_dir = os.path.dirname(os.path.abspath(__file__))


ffprofile = webdriver.FirefoxProfile(mylib.get_ffprofile_path("default"))
driver = webdriver.Firefox(executable_path=os.path.join(
    script_dir, "driver", "geckodriver.exe"), firefox_profile=ffprofile)

driver.get("https://www.yahoo.co.jp")
driver.close()
driver.quit()
