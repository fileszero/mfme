import datetime
import re
from typing import Dict, Tuple, List

from mfme_client import PaymentRecord, mfme_client
from os import replace
import mylib

from web_client import web_client

class order_item:
    name:str = ''
    price:int = 0
    qty:int = 0
    amount:int=0
    close_date:datetime.date=None
    def __init__(self,name:str,price:int,qty:int,amount:int,close_date:datetime.date ):
        self.name=name
        self.price=price
        self.qty=qty
        self.amount=amount
        self.close_date=close_date
        # rec={"name":name,"price":price,"qty":qty,"amount":amount,"close_date":close_date}

class coop_client(web_client):
    def __init__(self, config):
        super().__init__(config)

    def __del__(self):
        super().__del__()

    def login(self):
        login_url = "https://ouchi.ef.cws.coop/auth/bb/login.do?relayed=1"
        self.browser().get(login_url)

        # check already login
        already_login = self.browser().find_elements_by_xpath("//a[@title='ログアウト' and contains(text(), 'ログアウト')]")
        if len(already_login) != 0:
            return
        # todo


        # メールアドレスを入力
        e = self.browser().find_element_by_xpath("//input[@id='username']")
        e.clear()
        e.send_keys(self.email)

        # パスワードを入力
        e = self.browser().find_element_by_xpath("//input[@name='j_password']")
        e.clear()
        e.send_keys(self.password)

        # ログインボタンを押す
        self.clickByXPath("//input[@type='submit' and @value='ログイン']")

    def getOrderHistory(self) -> List[order_item]:
        # go home
        self.browser().get("https://ouchi.ef.cws.coop/ec/bb/ecTopInit.do")
        self.clickByXPath("//a[@title='ご注文履歴' and contains(text(), 'ご注文履歴')]")

        close_date_ele=self.browser().find_element_by_xpath("//div[@class='close_date']")
        close_date_txt=self.getTextByJS(close_date_ele)
        m = re.search(r'(\d+)月(\d+)日', close_date_txt).groups()
        today = datetime.date.today()
        close_date=datetime.date(today.year,int(m[0]),int(m[1]))
        # print(f"{close_date:%Y/%m/%d}")

        e=self.browser().find_element_by_xpath("//table[@class='standard']")

        rows = e.find_elements_by_xpath("//tr[@class='row_add' or @class='row_even']")
        recs=[]
        for row in rows:
            cols=row.find_elements_by_xpath('td')
            name=row.find_element_by_xpath("td/p[@class='name_clm']").text
            price_txt:str=row.find_element_by_xpath("td[@class='price_clm']").text
            price=mylib.to_int(price_txt.replace('円',''))
            qty_txt=row.find_element_by_xpath("td[@class='quantity_clm']").text
            qty=mylib.to_int(qty_txt)
            amount_txt=row.find_element_by_xpath("td[@class='amount_clm']").text
            amount=mylib.to_int(amount_txt.replace('円',''))
            rec=order_item(name,price,qty,amount,close_date)
            recs.append(rec)
            # print(rec)
        return recs


if __name__ == '__main__':

    config = mylib.get_config("coop.jsonc")

    c_client = coop_client(config["coop"])

    c_client.login()
    orders=c_client.getOrderHistory()

    mf_payments:List[PaymentRecord]=[]
    for order in orders:
        name_surfix=""
        if order.qty>1:
            name_surfix=f" ×{order.qty}"
        mf_payments.append(PaymentRecord(config["mfme"]["account"],order.close_date,order.name+name_surfix,order.amount,"食費","食費"))

    m_client = mfme_client(config["mfme"])
    m_client.login()
    m_client.AddPaymentRecord(mf_payments)

    val = input('END OF __main__')

