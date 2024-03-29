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
            total,billable,free = sbi.GetActualExecutionPriceOfToday()
            print(f"当日約定代金  手数料対象:{billable/10000:.1f} 万円 Free:{free/10000:.1f} 万円 合計: {total/10000:.1f} 万円" )
            continue

        code= params[0].strip()

        if not re.match(r'\d{4}',code):
            print('non stock code')
            continue
        quantity=0
        # special logics
        if(code in ["1360"]):    #日経平均ベア２倍上場投信
            quantity=200
        elif(code in ["2516"]):    #東証マザーズＥＴＦ
            quantity=100
        elif(code in ["1306"]):    #ＮＥＸＴ　ＦＵＮＤＳ　ＴＯＰＩＸ連動型上場投信
            quantity=50


        sbi.ActualBuyingIFDOCO(stockCode=code,quantity=quantity, profit=0.007,losscut=0.015,GyakuSashine=2)
    except Exception as e:
        print(e)

