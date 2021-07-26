from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


from pyvirtualdisplay import Display
import platform

import mylib




class web_client:
    _browser:webdriver.Firefox = None
    _display:Display = None

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

    def showInFront(self):
        self.browser().switch_to.window(self.browser().current_window_handle)
        self.browser().execute_script("window.focus();")
        # self.browser().fullscreen_window()

    def clickByXPath(self, xpath):
        WebDriverWait(self.browser(), 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath)))
        e = self.browser().find_element_by_xpath(xpath)
        e.click()

    def waitByXPath(self, xpath):
        WebDriverWait(self.browser(), 10).until(
            EC.presence_of_element_located((By.XPATH, xpath)))

    def inputByXPath(self, xpath,value):
        WebDriverWait(self.browser(), 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath)))
        e = self.browser().find_element_by_xpath(xpath)
        e.send_keys(value)

    def getTextByJS(self,element):
        script = "return arguments[0].innerText"
        txt=self.browser().execute_script(script,element)
        return txt