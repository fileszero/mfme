# -*- coding: utf-8 -*-

# https://selenium.dev/documentation/en/webdriver/driver_requirements/#firefox
# Simple assignment
import os
import json
import datetime
import math
import re
from dateutil.relativedelta import relativedelta
import mylib
from decimal import Decimal

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sqlite3
from pyvirtualdisplay import Display
import platform


class sbi_client:
    _browser = None
    _display = None

    def __init__(self, config):
        self.email = config["mail"]
        self.password = config["password"]
        self.tradePassword= config["tradePassword"]

    def __del__(self):
        if self._browser:
            self._browser.close()
        if self._display:
            self._display.sendstop()
            self._display.stop()

    def browser(self) -> webdriver:
        if platform.system() == 'Linux':
            if not self._display:
                self._display = Display(visible=0, size=(800, 600))
                self._display.start()
        if not self._browser:
            self._browser = webdriver.Firefox(executable_path=mylib.get_ff_executable_path(
            ), firefox_profile=mylib.get_ff_profile())
        return self._browser

    def waitByXPath(self, xpath):
        WebDriverWait(self.browser(), 10).until(
            EC.presence_of_element_located((By.XPATH, xpath)))

    def clickByXPath(self, xpath):
        WebDriverWait(self.browser(), 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath)))
        e = self.browser().find_element_by_xpath(xpath)
        e.click()

    def inputByXPath(self, xpath,value):
        WebDriverWait(self.browser(), 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath)))
        e = self.browser().find_element_by_xpath(xpath)
        e.send_keys(value)

    def login(self):
        self.browser().get("https://www.sbisec.co.jp/ETGate")
        # self.browser().get("https://id.moneyforward.com/sign_in/email")
        # already_login = self.browser().find_elements_by_xpath(
        #     "//div[contains(@class,'alert-success')][contains(text(), '既にログインしています')]")
        already_login = self.browser().find_elements_by_xpath("//img[@title='ログアウト']")
        if len(already_login) != 0:
            return

        # メールアドレスを入力
        e = self.browser().find_element_by_xpath("//input[@name='user_id']")
        #e = self.browser().find_element_by_id("sign_in_session_service_email")
        e.clear()
        e.send_keys(self.email)
        # パスワードを入力
        # //*[@id="password_input"]/input
        e = self.browser().find_element_by_xpath("//input[@name='user_password']")
        e.clear()
        e.send_keys(self.password)
        # ログインボタンを押す
        # //*[@id="SUBAREA01"]/form/div/div/div/p[2]/a/input
        self.clickByXPath("//input[@name='ACT_login']")
        # self.browser().get("https://site1.sbisec.co.jp/ETGate/")
        # frm = self.browser().find_element_by_name("commit")
        # frm.click()

        # wait
        self.waitByXPath("//img[@title='ログアウト']")

    def openStock(self, stockCode):
        url="https://site1.sbisec.co.jp/ETGate/" \
            f"?stock_sec_code_mul={stockCode}" \
            "&exchange_code=TKY" \
            f"&i_stock_sec={stockCode}" \
            "&i_exchange_code=TKY" \
            "&i_output_type=0" \
            "&i_dom_flg=1" \
            "&_ControlID=WPLETsiR001Control" \
            "&_PageID=WPLETsiR001Ilst10" \
            "&_ActionID=getDetailOfStockPriceJP" \
            "&getFlg=on"
        self.browser().get(url)
        # self.inputByXPath( '//*[@id="top_stock_sec"]',stockCode)
        # self.clickByXPath('//*[@id="srchK"]/a')
        e = self.browser().find_element_by_xpath('//*[@id="main"]//a[contains(text(), "ポートフォリオへ追加")]')
        e = self.browser().find_element_by_xpath('//h3/span[@class="fxx01"]')
        print(e.text)

    def minQuantity(self,unit:int,price:float,target:float):
        quantity = target/price
        return int(math.ceil(quantity / unit)) * unit

    def CreditBuyingIFDOCO(self, stockCode,quantity, stopOrder:Decimal,limitOrder:Decimal, profit:Decimal,losscut:Decimal):
        # self.openStock(stockCode)

        # # 売買単位
        # e = self.browser().find_element_by_xpath('//th[./p[contains(text(), "売買単位")]]/following-sibling::td')
        # unit= int(e.text)

        # self.clickByXPath('//*[@id="clmSubArea"]//a[contains(text(), "信用買")]')
        # # 現物
        # url="https://site1.sbisec.co.jp/ETGate/?" \
        #     "_ControlID=WPLETstT002Control" \
        #     "&_DataStoreID=DSWPLETstT002Control" \
        #     "&_PageID=DefaultPID" \
        #     "&getFlg=on" \
        #     "&_ActionID=DefaultAID" \
        #     f"&stock_sec_code={stockCode}" \
        #     "&market=TKY" \
        #     f"&stock_sec_code_mul={stockCode}" \
        #     "&mktlist=TKY" \
        #     "&trade_Market="
        #     # "&_SeqNo=1594774393721_default_task_469_WPLETsiR001Ilst10_getDetailOfStockPriceJP" \
        # 信用買
        url="https://site1.sbisec.co.jp/ETGate/?" \
            "_ControlID=WPLETstT005Control" \
            "&_DataStoreID=DSWPLETstT005Control" \
            "&_PageID=DefaultPID" \
            "&getFlg=on" \
            "&_ActionID=DefaultAID" \
            f"&stock_sec_code={stockCode}" \
            "&market=TKY" \
            f"&stock_sec_code_mul={stockCode}" \
            "&payment_limit=6"
            # "&_SeqNo=1594780715742_default_task_657_WPLETsiR001Iser10_clickToSearchStockPriceJP" \

        self.browser().get(url)
        self.clickByXPath('//*[@id="stocktype_ifdoco"]')

        # 銘柄名
        print(self.browser().find_element_by_xpath('//input[@name="official_jpn_comp_name"]').get_attribute("value"))

        # 売買単位
        e = self.browser().find_element_by_xpath('//td[contains(text(), "売買単位")]')
        innerHtml=self.browser().execute_script("return arguments[0].innerHTML",e)
        unit = int(re.findall(r'売買単位：\s*(\d+)\s*<',innerHtml)[0])
        print(unit)

        # autoUpdateXPath='//*[@id="imgRefArea_MTB0" and @title="稼働"]'
        # e = self.browser().find_elements_by_xpath(autoUpdateXPath)
        # if len(e) >0:
        #     self.clickByXPath(autoUpdateXPath)
        #     self.browser().find_elements_by_xpath('//*[@id="imgRefArea_MTB0" and @title="停止"]')

        # 現在値
        e = self.browser().find_element_by_xpath('//*[@id="HiddenTradePrice"]')
        cur_price= Decimal(self.browser().execute_script("return arguments[0].innerHTML",e))
        stopOrderPrice=cur_price + stopOrder    # 逆指値
        limitOrderPrice=cur_price + limitOrder  # 指値

        min_quantity=self.minQuantity(unit,stopOrderPrice,(100*10000)+10000)
        if( quantity<min_quantity):
            quantity=min_quantity

        # 株数
        e = self.browser().find_element_by_xpath('//*[@id="ifdoco_input_quantity"]')
        e.clear()
        e.send_keys(str(quantity))
        # 逆指値
        e = self.browser().find_element_by_xpath('//*[@id="gyakusashine_ifdoco"]')
        e.click()
        # 逆指値-価格 円 以上になった時点で
        e = self.browser().find_element_by_xpath('//*[@id="ifoco_input_trigger_price"]')
        e.send_keys(str(stopOrderPrice))
        # 逆指値-指値
        e = self.browser().find_element_by_xpath('//*[@id="gyakusashine_sashine_ifdoco_u"]')
        e.click()
        # 逆指値-指値-価格
        e = self.browser().find_element_by_xpath('//*[@id="ifoco_gsn_input_price"]')
        e.send_keys(str(limitOrderPrice))

        #期間
        e = self.browser().find_element_by_xpath('//input[@name="ifoco_selected_limit_in" and @value="this_day"]')
        e.click()

        # 信用取引区分 日計り
        e = self.browser().find_element_by_xpath('//*[@id="ifdoco_payment_limit_labelD"]')
        e.click()

        # OCO1 利益確定
        e = self.browser().find_element_by_xpath('//*[@id="doneoco1_input_price"]')
        e.send_keys(str(round( stopOrderPrice+profit,1)))

        # OCO2 損切
        e = self.browser().find_element_by_xpath('//*[@id="doneoco2_input_trigger_price"]')
        e.send_keys(str(limitOrderPrice+losscut))
        e = self.browser().find_element_by_xpath('//*[@id="nariyuki_ifdoco"]')
        e.click()

        # 取引PW
        e = self.browser().find_element_by_xpath('//*[@id="pwd3"]')
        e.send_keys(self.tradePassword)

        # 注文確認画面へ
        self.clickByXPath('//a[@id="botton1"]')

        # 記録
        # ss_name=f"{stockCode}_.png"
        # self.browser().save_screenshot(ss_name)