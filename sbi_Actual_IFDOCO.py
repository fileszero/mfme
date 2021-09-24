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
    try:
        with open(prompt_file) as f:
            print(f.read())

        val = input('現物買 IFDOCO Enter Code:')
        sbi.login()
        params= val.split()
        #reload params
        sbi_config = mylib.get_config("sbi.jsonc")
        if len(params)==0:
            total = sbi.GetActualExecutionPriceOfToday()
            print(f"当日約定代金合計: {total/10000} 万円" )
            continue

        code= params[0].strip()

        if not re.match(r'\d{4}',code):
            print('non stock code')
            continue
        sbi.ActualBuyingIFDOCO(stockCode=code,profit=0.007,losscut=0.03,GyakuSashine=2)
    except Exception as e:
        print(e)

