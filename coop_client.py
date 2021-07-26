import mylib

from web_client import web_client


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

    def getOrderHistory(self):
        # go home
        self.browser().get("https://ouchi.ef.cws.coop/ec/bb/ecTopInit.do")
        self.clickByXPath("//a[@title='ご注文履歴' and contains(text(), 'ご注文履歴')]")

        close_date=self.browser().find_element_by_xpath("//div[@class='close_date']")

        e=self.browser().find_element_by_xpath("//table[@class='standard']")

        rows = e.find_elements_by_xpath("//tr[@class='row_add' or @class='row_even']")
        for row in rows:
            cols=row.find_elements_by_xpath('td')
            name=row.find_element_by_xpath("td/p[@class='name_clm']").text
            price=row.find_element_by_xpath("td[@class='price_clm']").text
            qty=row.find_element_by_xpath("td[@class='quantity_clm']").text
            amount=row.find_element_by_xpath("td[@class='amount_clm']").text
            print(name)
            print(price)
            print(qty)
            print(amount)

if __name__ == '__main__':

    config = mylib.get_config("coop.jsonc")

    client = coop_client(config["coop"])

    client.login()
    client.getOrderHistory()
    # sbi.ActualBuyingIFDOCO(7513,quantity=0)
    # sbi.GetOrders()
    # sbi.openChart('5929')
    val = input('END OF __main__')

