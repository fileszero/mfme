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
    val = input('Enter Code:')
    params= val.split()
    #reload params
    sbi_config = mylib.get_config("sbi.jsonc")
    if params[0] in sbi_config["CreditBuyingIFDOCO"]:
        criteria=sbi_config["CreditBuyingIFDOCO"][params[0]]
        stopOrder=Decimal(str(criteria["stopOrder"]))
        limitOrder=Decimal(str(criteria["limitOrder"]))
        if len(params)>=2:
            stop_limit_diff= stopOrder-limitOrder
            stopOrder=Decimal(str(params[1]))
            limitOrder=stopOrder-stop_limit_diff

        sbi.CreditBuyingIFDOCO(criteria["code"],criteria["quantity"],stopOrder,limitOrder,Decimal(str(criteria["profit"])),Decimal(str(criteria["losscut"])))
    else:
        print("No stockcode definition")