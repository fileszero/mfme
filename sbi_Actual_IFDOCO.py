# -*- coding: utf-8 -*-

# https://selenium.dev/documentation/en/webdriver/driver_requirements/#firefox
# Simple assignment
import os
import json
import slack
import sys
import re

from decimal import Decimal

import mylib
import sbi_client

sbi_config = mylib.get_config("sbi.jsonc")

sbi = sbi_client.sbi_client(sbi_config["sbi"])

sbi.login()
# sbi.openStock('9984')
script_dir = os.path.dirname(os.path.abspath(__file__))
prompt_file = os.path.join(script_dir, 'BuyRule.txt')

while True:
    with open(prompt_file) as f:
        print(f.read())

    val = input('現物買 IFDOCO Enter Code:')
    params= val.split()
    #reload params
    sbi_config = mylib.get_config("sbi.jsonc")
    code= params[0].strip()

    if not re.match(r'\d{4}',code):
        print('non stock code')
        continue
    try:
        sbi.ActualBuyingIFDOCO(stockCode=code,profit=0.02,losscut=0.03)
    except Exception as e:
        print(e)

