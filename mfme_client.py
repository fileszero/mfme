# -*- coding: utf-8 -*-

# https://selenium.dev/documentation/en/webdriver/driver_requirements/#firefox
# Simple assignment
import os
import json
import datetime
from dateutil.relativedelta import relativedelta
import mylib

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sqlite3
from pyvirtualdisplay import Display
import platform


class mfme_client:
    _browser = None
    _display = None

    def __init__(self, config):
        self.email = config["mail"]
        self.password = config["password"]

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

    def login(self):
        self.browser().get("https://moneyforward.com/")
        # self.browser().get("https://id.moneyforward.com/sign_in/email")
        # already_login = self.browser().find_elements_by_xpath(
        #     "//div[contains(@class,'alert-success')][contains(text(), '既にログインしています')]")
        already_login = self.browser().find_elements_by_xpath("//a[@href='/users/sign_out']")
        if len(already_login) != 0:
            return
        # メールでログインに移動
        self.clickByXPath("//a[@href='/users/sign_in']")
        self.clickByXPath("//a[contains(@href, '/sign_in/email')]")

        # メールアドレスを入力
        e = self.browser().find_element_by_xpath("//input[@name='mfid_user[email]']")
        #e = self.browser().find_element_by_id("sign_in_session_service_email")
        e.clear()
        e.send_keys(self.email)
        self.clickByXPath("//input[@type='submit']")
        # パスワードを入力
        e = self.browser().find_element_by_xpath("//input[@name='mfid_user[password]']")
        # e = self.browser().find_element_by_id("sign_in_session_service_password")
        e.clear()
        e.send_keys(self.password)
        # ログインボタンを押す
        self.clickByXPath("//input[@type='submit']")
        self.browser().get("https://moneyforward.com/")
        # frm = self.browser().find_element_by_name("commit")
        # frm.click()

    def clickByXPath(self, xpath):
        WebDriverWait(self.browser(), 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath)))
        e = self.browser().find_element_by_xpath(xpath)
        e.click()

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
            for m in range(months):
                curdate = basedate + relativedelta(months=-m)
                print(curdate)
                self.gotoYearMonth(curdate.year, curdate.month)
                self.downloadCSV()
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
