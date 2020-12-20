# -*- coding: utf-8 -*-

# https://selenium.dev/documentation/en/webdriver/driver_requirements/#firefox
# Simple assignment
import os
import json
import slack
import sys

from decimal import Decimal

import mylib
import sbi_client

sbi_config = mylib.get_config("sbi.jsonc")

sbi = sbi_client.sbi_client(sbi_config["sbi"])

sbi.login()
# sbi.openStock('9984')

while True:
    val = input('現物買 IFDOCO Enter Code:')
    params= val.split()
    #reload params
    sbi_config = mylib.get_config("sbi.jsonc")
    try:
        sbi.ActualBuyingIFDOCO(params[0])
    except Exception as e:
        print(e)

