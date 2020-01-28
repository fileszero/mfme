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
import mfme_client

import glob
import pandas as pd  # pip install pandas

me_config = mylib.get_config()

os.makedirs(me_config["workdir"],exist_ok=True)

mfme = mfme_client.mfme_client(me_config)
# mfme.updateLatestCSV()

conn = sqlite3.connect(me_config["dbfile"])
cur = conn.cursor()
# personsというtableを作成してみる
# 大文字部はSQL文。小文字でも問題ない。
cur.execute(
    """CREATE TABLE IF NOT EXISTS IncomeOutgo (
        IsTarget INTEGER,
        Date datetime,
        Detail  TEXT,
        Amount  INTEGER,
        Account TEXT,
        Class1 TEXT,
        Class2 TEXT,
        Memo TEXT,
        IsTransfer INTEGER,
        MFId TEXT PRIMARY KEY
     ) """)

files = glob.glob(os.path.join(mfme.workdir, "*.csv"))
print(files)
for f in files:
    df = pd.read_csv(f, encoding="SHIFT-JIS")
    df.to_sql("import_work", conn, if_exists="replace")
    insetrt_sql = """
    INSERT INTO IncomeOutgo(IsTarget,Date,Detail,Amount,Account,Class1,Class2,Memo,IsTransfer,MFId)
    SELECT "計算対象","日付","内容","金額（円）","保有金融機関","大項目","中項目","メモ","振替","ID"
        FROM import_work WHERE "ID" NOT IN (SELECT MFId FROM IncomeOutgo)
    """
    cur.execute(insetrt_sql)
    os.remove(f)

df = pd.read_sql(
    "select * from IncomeOutgo "
    + "WHERE IsTarget=1 AND IsTransfer=0"
    , conn)

# https: // note.nkmk.me/python-pandas-datetime-timestamp/
print(pd.to_datetime(df["Date"]))
df["Date"]=pd.to_datetime(df["Date"])
df['Year'] = df["Date"].dt.year
df['Month'] = df["Date"].dt.month
pt = pd.pivot_table(df, index=["Account", "Detail"], columns=["Year","Month"], aggfunc='sum', values="Amount",fill_value="")
pt.sort_values(by=["Account", "Detail"], inplace=True)
pd.set_option('display.max_rows', None)
print(pt.to_html())
conn.close()
# browser.close()
