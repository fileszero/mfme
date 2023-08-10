# -*- coding: utf-8 -*-

# https://selenium.dev/documentation/en/webdriver/driver_requirements/#firefox
# Simple assignment
from multiprocessing import Array
import os
import json
import datetime
import re
import time
from tokenize import String
from dateutil.relativedelta import relativedelta
import mylib

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import sqlite3
from pyvirtualdisplay import Display
import platform

from typing import List

from web_client import web_client
class PaymentRecord:
    account:str
    payment_date:datetime.date
    name:str
    amount:int
    category:str
    sub_category:str

    def __init__(self,account:str,payment_date:datetime.date, name:str,amount:int,category:str,sub_category:str) -> None:
        self.account=account
        self.payment_date=payment_date
        self.name=name
        self.amount=amount
        self.category=category
        self.sub_category=sub_category

class mfme_client(web_client):
    _group_name:str="グループ選択なし"
    def __init__(self, config):
        super().__init__(config)
        self._group_name=config.get("group",self._group_name)

    def __del__(self):
        super().__del__()

    def login(self):
        retry=10
        while retry>0:
            try:
                self.browser().get("https://moneyforward.com/")
                # self.browser().get("https://id.moneyforward.com/sign_in/email")
                # already_login = self.browser().find_elements_by_xpath(
                #     "//div[contains(@class,'alert-success')][contains(text(), '既にログインしています')]")
                already_login = self.browser().find_elements_by_xpath("//a[@href='/sign_out']")
                if len(already_login) != 0:
                    return
                # メールでログインに移動
                self.clickByXPath("//a[@href='/sign_in']")
                self.clickByXPath("//a[contains(@href, '/sign_in/email')]")

                # メールアドレスを入力
                e = self.browser().find_element_by_xpath("//input[@name='mfid_user[email]']")
                #e = self.browser().find_element_by_id("sign_in_session_service_email")
                e.clear()
                e.send_keys(self.email)
                # self.clickByXPath("//input[@type='submit']")
                self.clickByXPath("//*[@id='submitto']")

                # パスワードを入力
                e = self.browser().find_element_by_xpath("//input[@name='mfid_user[password]']")
                # e = self.browser().find_element_by_id("sign_in_session_service_password")
                e.clear()
                e.send_keys(self.password)
                # ログインボタンを押す
                # self.clickByXPath("//input[@type='submit']")
                self.clickByXPath("//*[@id='submitto']")
                self.browser().get("https://moneyforward.com/")

                # 待機
                already_login = self.browser().find_elements_by_xpath("//a[@href='/users/sign_out']")

                # frm = self.browser().find_element_by_name("commit")
                # frm.click()
                #グループ変更
                e = self.browser().find_element_by_xpath('//*[@id="group_id_hash"]')
                select=Select(e)
                select.select_by_visible_text( self._group_name )
                retry=-1
                print("login success")
            except Exception as e:
                retry -= 1
                print("login error")
                print(e)

    def chnageGroup(self,groupName:str):
        # Home
        self.browser().get("https://moneyforward.com/")
        e = self.browser().find_element_by_xpath('//*[@id="group_id_hash"]')
        select=Select(e)
        select.select_by_visible_text( groupName )


    def gotoYearMonth(self, year: int, month: int):
        # 家計簿
        self.browser().get("https://moneyforward.com/cf")
        # 月を選択
        self.clickByXPath("//*[contains(text(), '月を選択')]")

        try:
            self.clickByXPath(
                f"//li[contains(@class,'js-dropdown-select-year-item')][@data-year='{year}']")

            self.clickByXPath(
                f"//li[contains(@class,'js-fc-year-month-dropdown-item')][@data-year='{year}'][@data-month='{month}']")
            # http://www.stockdog.work/entry/2018/06/29/202701
            self.browser().implicitly_wait(1)
            WebDriverWait(self.browser(), 30).until_not(EC.presence_of_element_located(
                (By.XPATH, "//h2[contains(text(), 'Loading...')]")))
        except (NoSuchElementException) as e:
            print("no month link:" + e.msg)

    def downloadCSV(self):
        self.clickByXPath("//*[@id='js-dl-area']")
        self.clickByXPath("//*[@id='js-csv-dl']")

    def getCSV(self, year, month):
        # https://moneyforward.com/cf/csv?from=2019%2F10%2F01
        self.browser().get("https://moneyforward.com/cf/")
        self.browser().get(
            f"https://moneyforward.com/cf/csv?from={year}%2F{month}%2F01")

    # main

    def updateLatestCSV(self, months: int = 3):
        try:
            self.login()
            basedate = datetime.datetime.now().replace(day=1)
            # 家計簿
            self.browser().get("https://moneyforward.com/cf")
            # self.clickByXPath("//span[contains(@class,'fc-button-today')][contains(text(), '今月')]")
            for m in range(months):
                # curdate = basedate + relativedelta(months=-m)
                # print(curdate)
                # self.gotoYearMonth(curdate.year, curdate.month)
                self.downloadCSV()
                self.clickByXPath("//span[contains(@class,'fc-button-prev')][contains(., '◄')]")
                self.browser().implicitly_wait(1)
                WebDriverWait(self.browser(), 30).until_not(EC.presence_of_element_located(
                    (By.XPATH, "//h2[contains(text(), 'Loading...')]")))
                # getCSV(curdate.year, curdate.month)
        except:
            if self._browser:
                self._browser.save_screenshot("ss_updateLatestCSV.png")

    def updateBSHistoryCSV(self):
        try:
            self.login()
            self.browser().get("https://moneyforward.com/bs/history")
            self.browser().execute_script(
                'window.document.getElementById("floating-feedback-box").style.display="none";')
            self.clickByXPath("//i[@class='icon-download-alt']")
            self.clickByXPath("//a[@href='/bs/history/csv']")
        except Exception as e:
            print(e)
            if self._browser:
                self._browser.save_screenshot("ss_updateBSHistoryCSV.png")

    def MFAVerify(self, url):
        self.login()
        self.browser().get(url)

    def AddPaymentRecord(self,recs:List[PaymentRecord]):
        self.browser().implicitly_wait(8)   #wait
        # url="https://moneyforward.com/accounts/show_manual/" + account
        url="https://moneyforward.com/cf"
        self.browser().get(url)
        self.clickByXPath("//button[@href='#user_asset_act_new']")
        self.browser().implicitly_wait(7)   #wait

        for rec in recs:
            print(rec.name)
            # 日付
            e = self.browser().find_element_by_xpath("//input[@id='updated-at']")
            e.clear()
            e.send_keys(f"{rec.payment_date:%Y/%m/%d}")
            self.clickByXPath("//div[@id='amount-important']")   #close calendar

            # 金額
            e = self.browser().find_element_by_xpath("//input[@id='appendedPrependedInput']")
            e.clear()
            e.send_keys(rec.amount)

            #支払い元（財布）
            e = self.browser().find_element_by_xpath("//select[@id='user_asset_act_sub_account_id_hash']")
            account_selector=Select(e)
            for idx,option in enumerate(account_selector.options):
                if option.text[:len(rec.account)]==rec.account: # 選択肢のテキスト
                    account_selector.select_by_index(idx)
                    break



            #大分類
            self.clickByXPath("//a[@id='js-large-category-selected']")
            e = self.browser().find_element_by_xpath("//div[@id='large_category_group']")
            cat=e.find_element_by_link_text(rec.category)
            cat.click()
            #中分類
            self.clickByXPath("//a[@id='js-middle-category-selected']")
            e = self.browser().find_element_by_xpath("//div[@id='target-js-content-field']")
            cat=e.find_element_by_link_text(rec.sub_category)
            cat.click()

            # 内容
            e = self.browser().find_element_by_xpath("//input[@id='js-content-field']")
            e.clear()
            e.send_keys(rec.name)

            #保存
            self.clickByXPath("//input[@type='submit' and @id='submit-button']")
            # 3秒待機
            # time.sleep(3)
            self.clickByXPath("//input[@type='button' and @id='confirmation-button']")  #続けて入力する

        self.clickByXPath("//div[@class='close' and @type='button' and @data-dismiss='modal']")

    def requery_account(self, account_ids:List[str]):
        self.login()
        self.browser().get("https://moneyforward.com/accounts")
        for account_id in account_ids:
            try:
                self.clickByXPath(f"//*[@id='js-recorrect-form-{account_id}']/input")
            except Exception as e:
                print(e)
            time.sleep(2)



if __name__ == '__main__':

    mfme_config = mylib.get_config("coop.jsonc")

    client = mfme_client(mfme_config["mfme"])

    client.login()
    # sbi.ActualBuyingIFDOCO(7513,quantity=0)
    # sbi.GetOrders()
    # sbi.openChart('5929')
    data=[]
    for i in range(3):
        data.append(PaymentRecord(mfme_config["mfme"]["account"],datetime.date(2021,7,27),f"てすと{i}","123","食費","食費"))
    client.AddPaymentRecord(data)
    val = input('END OF __main__')

