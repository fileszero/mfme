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
from selenium.webdriver.support.select import Select
import sqlite3
from pyvirtualdisplay import Display
import platform
import uuid

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

    def showInFront(self):
        self.browser().switch_to.window(self.browser().current_window_handle)
        self.browser().execute_script("window.focus();")
        # self.browser().fullscreen_window()

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

    # 現物買
    def ActualBuyingIFDOCO(self, stockCode,quantity=0, profit:float=0.05,losscut:float=0.03):
        self.showInFront()
        # 現物買
        url="https://site1.sbisec.co.jp/ETGate/?" \
            "_ControlID=WPLETstT002Control" \
            "&_DataStoreID=DSWPLETstT002Control" \
            "&_PageID=DefaultPID" \
            "&getFlg=on" \
            "&_ActionID=DefaultAID" \
            f"&stock_sec_code={stockCode}" \
            "&market=TKY" \
            f"&stock_sec_code_mul={stockCode}" \
            "&mktlist=TKY" \
            "&trade_Market="
            # "&_SeqNo=1606181946998_default_task_221_WPLETacR001Rlst10_detail_kabu_1" \
        self.browser().get(url)
        self.clickByXPath('//*[@id="stocktype_ifdoco"]')    #IFDOCO

        # 銘柄名
        e = self.browser().find_element_by_xpath('//h3/span[@style="font-weight:bold;font-size:18px;"]')
        print(e.text)


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
        #買い気配
        ita_info = self.browser().find_elements_by_xpath('//*[@id="posElem_370"]/table/tbody/tr')
        sell_kehai_min=None
        buy_kehai_max=None
        kehai_price_prev=None
        trade_scale=Decimal( 100000 )
        for kehai in ita_info:
            cols=kehai.find_elements_by_xpath('td')
            sell_kehai=mylib.to_dec( cols[0].text )
            kehai_price=mylib.to_dec( cols[1].text )
            buy_kehai=mylib.to_dec( cols[2].text )
            if kehai_price is not None:
                if sell_kehai is not None:
                    sell_kehai_min=kehai_price
                if buy_kehai_max is None and buy_kehai is not None:
                    buy_kehai_max=kehai_price
            if kehai_price_prev is not None and kehai_price is not None:
                if trade_scale > (kehai_price_prev-kehai_price):
                    trade_scale = kehai_price_prev-kehai_price
            kehai_price_prev=kehai_price
            # print( kehai )
        # 購入価格　決定
        if all([sell_kehai_min, buy_kehai_max ,trade_scale]):
            if(buy_kehai_max +trade_scale)<sell_kehai_min:
                cur_price=buy_kehai_max + trade_scale
            elif sell_kehai_min<cur_price:
                cur_price=sell_kehai_min

        # 株数
        if( quantity<unit):
            quantity=unit
        e = self.browser().find_element_by_xpath('//*[@id="ifdoco_input_quantity"]')
        e.clear()
        e.send_keys(str(quantity))
        # 指値
        e = self.browser().find_element_by_xpath('//*[@id="sashine_ifdoco_u"]')
        e.click()
        # 価格
        e = self.browser().find_element_by_xpath('//*[@id="ifoco_input_price"]')
        e.clear()
        e.send_keys(str(cur_price))

        #期間
        e = self.browser().find_element_by_xpath('//input[@name="ifoco_selected_limit_in" and @value="this_day"]')
        e.click()

        # 預り区分 特定預り
        e = self.browser().find_element_by_xpath('//input[@name="ifdoco_hitokutei_trade_kbn" and @value="0"]')
        e.click()


        # OCO1 利益確定
        e = self.browser().find_element_by_xpath('//*[@id="doneoco1_input_price"]')
        profit_diff=mylib.RoundHalfUp((float(cur_price)*profit),0)
        # if(profit_diff>50):
        #     profit_diff = 50
        profit_price=mylib.RoundHalfUp( float(cur_price) + float(profit_diff),0)
        e.send_keys(str(profit_price))

        # OCO2 損切
        e = self.browser().find_element_by_xpath('//*[@id="doneoco2_input_trigger_price"]')
        losscut_diff=mylib.RoundHalfUp( (float(cur_price)*losscut),0)
        # if(losscut_diff>profit_diff/2):
        #     losscut_diff=profit_diff/2
        losscut_price=mylib.RoundHalfUp( float(cur_price) - float(losscut_diff),0)
        e.send_keys(str(losscut_price))
        e = self.browser().find_element_by_xpath('//*[@id="nariyuki_ifdoco"]')  #成行 で執行
        e.click()

        #期間
        e = self.browser().find_element_by_xpath('//input[@name="doneoco_selected_limit_in" and @value="kikan"]')   #期間指定
        e.click()
        # 日付
        e = self.browser().find_element_by_xpath('//select[@name="doneoco_limit_in"]')   #期間指定
        select=Select(e)
        select.select_by_index( len(select.options)-1 )


        # 取引PW
        e = self.browser().find_element_by_xpath('//*[@id="pwd3"]')
        e.send_keys(self.tradePassword)


        # 注文確認画面へ
        self.clickByXPath('//a[@id="botton1"]')

        # 記録
        # ss_name=f"{stockCode}_.png"
        # self.browser().save_screenshot(ss_name)

    def GetOrders(self):
        url = "https://site1.sbisec.co.jp/ETGate/?_ControlID=WPLETstT013Control" \
            "&_PageID=DefaultPID" \
            "&_DataStoreID=DSWPLETstT013Control" \
            "&getFlg=on" \
            "&_ActionID=DefaultAID"
            # "&_SeqNo=1596757675532_default_task_488_WPLETstT005Best10_place" /

        self.browser().get(url)
        recs = self.browser().find_elements_by_xpath('//form[@action="/ETGate/"]//table[contains(@class, "md-l-table-01")]/*/tr')
        for idx, rec in enumerate(recs[5:]):
            mode=idx%3
            cols=rec.find_elements_by_tag_name('td')
            if mode==0:
                stockCode=cols[0].text
                status=cols[1].text
                orderType=cols[2].text
                stockName=cols[3].text
                cancel_link=cols[4].find_element_by_xpath('a[contains(.,"取消")]')
                edit_link=cols[4].find_element_by_xpath('a[contains(.,"訂正")]')
            print(idx)

    def openChart(self, stockCode):
        hash=str(uuid.uuid4()).replace('-','')
        url="https://mchart.iris.sbisec.co.jp/sbi/gchart/gc2/chart" \
        f"?ricCode={stockCode}.T" \
        "&style=main_domestic_chart" \
        "&size=0" \
        "&type=real" \
        f"&hash={hash}" \
        "&investor=customer"
        self.browser().get(url)

    # 現物約定代金合計を取得
    def GetActualExecutionPriceOfToday(self):
        url="https://site1.sbisec.co.jp/ETGate/WPLETagR001Control/DefaultPID/DefaultAID"
        self.browser().get(url)
        self.clickByXPath('//a[contains(text(),"国内株式(現物)") and @class="wlink"]')

        col=self.browser().find_element_by_xpath("//td[string()='受渡金額/決済損益（日計り分）']")
        #table=sbi.browser().find_element_by_xpath("//td[contains(string(),'受渡金額/決済損益（日計り分）')]/parent::tr//parent::table")
        table=col.find_element_by_xpath('../..')
        rows=table.find_elements_by_xpath('tr')
        total:int = 0
        for idx, row in enumerate(rows[1:]):
            cols=row.find_elements_by_tag_name('td')
            col_offset=0
            if len(cols)!=9:
                col_offset=-1
            buy_sell_cell=cols[1+col_offset]
            price_cell=cols[7+col_offset]

            price=mylib.to_int(price_cell.text.split()[0])
            # print(price)
            total += price
        return total

if __name__ == '__main__':

    sbi_config = mylib.get_config("sbi.jsonc")

    sbi = sbi_client(sbi_config["sbi"])

    sbi.login()
    # sbi.ActualBuyingIFDOCO(7513,quantity=0)
    # sbi.GetOrders()
    # sbi.openChart('5929')
    total=sbi.GetActualExecutionPriceOfToday()
    print(total)

    val = input('END OF __main__')
