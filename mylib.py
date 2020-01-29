# -*- coding: utf-8 -*-

import os
import sys
import json

from selenium import webdriver

_me_config = None

# https://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.firefox.firefox_profile


def get_ffprofile_path(profile):
    # ffprofile=webdriver.FirefoxProfile(os.path.join(os.environ['APPDATA'],"Mozilla","firefox","profiles","t0nhkhax.default"))
    FF_PROFILE_PATH = os.path.join(
        os.environ['APPDATA'], 'Mozilla', 'Firefox', 'Profiles')

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
    return os.path.join(FF_PROFILE_PATH, loc)


def get_config():
    global _me_config
    if not _me_config:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, "me.json")
        with open(json_path, "r") as fp:
            _me_config = json.load(fp)
    return _me_config


def get_ff_executable_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, "driver", "geckodriver.exe")


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
