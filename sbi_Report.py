# -*- coding: utf-8 -*-

# https://selenium.dev/documentation/en/webdriver/driver_requirements/#firefox
# Simple assignment
import os
import json
import sys
import time

from decimal import Decimal

import mylib
import sbi_client

from decimal import Decimal

import mylib
import sbi_client

sbi_config = mylib.get_config("sbi.jsonc")

sbi = sbi_client.sbi_client(sbi_config["sbi"])

sbi.login()
sbi.openStock('8267')
e = sbi.browser().find_element_by_xpath('//a[text()="チャート"]')
e.click()
# https://kurozumi.github.io/selenium-python/navigating.html#moving-between-windows-and-frames
frame=sbi.browser().find_element_by_xpath('//iframe')
sbi.browser().switch_to.frame(frame)
e = sbi.browser().find_element_by_xpath('//input[@id="resetChart"]')
e.click()

# sbi.browser().execute_script("document.getElementById('tippingPoint')")
e = sbi.browser().find_element_by_xpath('//li/a[text()="3ヶ月"]')
e.click()

e=sbi.browser().find_element_by_xpath('//img[@id="chartImg"]')
e.click()
e.click()


while True:
    e=sbi.browser().find_element_by_xpath('//input[@id="tippingPoint"]')
    e.click()
    checked=e.get_attribute('checked')
    if(checked):
        break


sbi.browser().switch_to.default_content()


# val = input('Enter Code:')

