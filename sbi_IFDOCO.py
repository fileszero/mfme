# -*- coding: utf-8 -*-

# https://selenium.dev/documentation/en/webdriver/driver_requirements/#firefox
# Simple assignment
import os
import json
import slack
import sys

import mylib
import sbi_client

sbi_config = mylib.get_config("sbi.json")

sbi = sbi_client.sbi_client(sbi_config["sbi"])

sbi.login()
# sbi.openStock('9984')
while True:
    val = input('Enter Code:')
    params= val.split()
    sbi.CreditBuyingIFDOCO(params[0])