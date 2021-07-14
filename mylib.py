# -*- coding: utf-8 -*-

import os
import sys
import select
import json
import re
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
import platform
from selenium import webdriver

from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN

_me_config = None

# https://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.firefox.firefox_profile


def get_ffdriver_filename():
    if platform.system() == 'Linux':
        return 'geckodriver'
    return 'geckodriver.exe'


def get_ffprofile_path(profile):
    # ffprofile=webdriver.FirefoxProfile(os.path.join(os.environ['APPDATA'],"Mozilla","firefox","profiles","t0nhkhax.default"))
    if(os.environ.get('APPDATA')):
        FF_PROFILE_PATH = os.path.join(
            os.environ['APPDATA'], 'Mozilla', 'Firefox', 'Profiles')
    if platform.system() == 'Linux':
        if(os.environ.get('HOME')):
            # /home/<username>/.mozilla/firefox/xxxxxxxx.default
            FF_PROFILE_PATH = os.path.join(
                os.environ['HOME'], '.mozilla', 'firefox')

    loc = None
    try:
        profiles = os.listdir(FF_PROFILE_PATH)
    except WindowsError:
        print("Could not find profiles directory.")
        sys.exit(1)
    try:
        for folder in profiles:
            print(folder)
            if folder.endswith(profile):
                loc = folder
    except StopIteration:
        print("Firefox profile not found.")
        sys.exit(1)
    path = None
    if loc:
        path = os.path.join(FF_PROFILE_PATH, loc)
    print(path)
    return path


def jsonc_to_json(string):
    # ブロックコメント除去
    string = re.sub(r'/\*.*?\*/', r'', string, flags=re.DOTALL)

    # ラインコメント除去
    string = re.sub(r'//.*\n', r'\n', string)
    return '\n'.join(filter(lambda x: x.strip(), string.split('\n')))

def get_config(filename='me.json'):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, filename)
    with open(json_path, "r", encoding="utf-8") as fp:
        jsonc=fp.read()
        config = json.loads( jsonc_to_json(jsonc))
        return config

def get_ff_executable_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, "driver", get_ffdriver_filename())


def get_ff_profile() -> webdriver.FirefoxProfile:
    config = get_config()
    # https://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.firefox.firefox_profile

    profile = webdriver.FirefoxProfile(get_ffprofile_path("default"))
    # https: // developer.mozilla.org/ja/docs/Download_Manager_preferences
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir",  config["workdir"])
    profile.set_preference("browser.download.useDownloadDir", True)
    # https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/downloads/FilenameConflictAction
    # http://dir.hatenablog.com/entry/downloadCsv
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk",
                           "text/plain,application/vnd.ms-excel, text/csv,text/comma-separated-values, application/octet-stream")
    profile.set_preference("browser.helperApps.neverAsk.openFile",
                           "text/csv,application/x-msexcel,application/excel,application/x-excel,application/vnd.ms-excel,image/png,image/jpeg,text/html,text/plain,application/msword,application/xml")
    profile.set_preference(
        "browser.download.manager.showAlertOnComplete", False)
    profile.set_preference("browser.download.manager.closeWhenDone", False)
    profile.set_preference("browser.download.manager.useWindow", False)
    profile.set_preference("browser.download.manager.focusWhenStarting", False)
    profile.set_preference("browser.download.manager.alertOnEXEOpen", False)
    profile.set_preference("pdfjs.disabled", True)

    return profile


def get_end_of_month(cur: date) -> date:
    som = cur.replace(day=1) + relativedelta(months=1) + relativedelta(days=-1)
    return som

def RoundHalfUp(val,digits) -> Decimal :
    # https://note.nkmk.me/python-round-decimal-quantize/
    format="0"
    if( digits>0):
        format="0." + ("0"*(digits-1))+"1"

    return Decimal(str(val)).quantize(Decimal(format), rounding=ROUND_HALF_UP)

def inputTimeOut(prompt:str, timeout_sec:int):
    print(prompt)
    # https://gist.github.com/atupal/5865237
    i, o, e = select.select( [sys.stdin], [], [], timeout_sec )
    if (i):
        return sys.stdin.readline().strip()
    else:
        return ''

def to_int(self,s:str,default=None) -> int:
    try:
        return int(s.replace(',', '').strip())
    except:
        return default

def to_dec(self,s:str,default=None) -> Decimal:
    try:
        return Decimal(s.replace(',', '').strip())
    except:
        return default

def unit_floor(v:Decimal,unit:Decimal)->Decimal:
    qv=v.quantize(Decimal("0.001"))
    qunit=unit.quantize(Decimal("0.001"))
    return (qv//qunit)*qunit

def unit_ceil(v:Decimal,unit:Decimal)->Decimal:
    qv=v.quantize(Decimal("0.001"))
    qunit=unit.quantize(Decimal("0.001"))
    c=(qv//qunit)*qunit
    if qv-c != 0:
        c+=qunit
    return c

def unit_round(v:Decimal,unit:Decimal)->Decimal:
    qv=v.quantize(Decimal("0.001"))
    qunit=unit.quantize(Decimal("0.001"))
    c=(qv//qunit)*qunit
    if (qv-c)*2>unit != 0:
        c+=qunit
    return c


if __name__ == '__main__':
    unit_ceil(Decimal(123.4),Decimal(0.4))
    unit_round(Decimal(122),Decimal(5))
    unit_round(Decimal(123),Decimal(5))
