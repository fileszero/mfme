# -*- coding: utf-8 -*-

# https://selenium.dev/documentation/en/webdriver/driver_requirements/#firefox
# Simple assignment
import os
import json
import slack

from datetime import date
from datetime import datetime

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

os.makedirs(me_config["workdir"], exist_ok=True)

mfme = mfme_client.mfme_client(me_config["mfme"])
mfme.updateLatestCSV()

conn = sqlite3.connect(me_config["dbfile"])
cur = conn.cursor()

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

files = glob.glob(os.path.join(me_config["workdir"], "*.csv"))
# print(files)
for f in files:
    df = pd.read_csv(f, encoding="SHIFT-JIS")
    df.to_sql("import_work", conn, if_exists="replace")
    insetrt_sql = """
    INSERT INTO IncomeOutgo(IsTarget,Date,Detail,Amount,Account,Class1,Class2,Memo,IsTransfer,MFId)
    SELECT "計算対象","日付","内容","金額（円）","保有金融機関","大項目","中項目","メモ","振替","ID"
        FROM import_work WHERE "ID" NOT IN (SELECT MFId FROM IncomeOutgo)
    """
    cur.execute(insetrt_sql)
    conn.commit()
    os.remove(f)

basedate = datetime.combine(date.today().replace(day=1), datetime.min.time())
# print(basedate)

datefrom = basedate + relativedelta(months=-12)
account_list = "'" + "','".join(me_config["mfme"]["reportAccount"]) + "'"
sql = ("select * from IncomeOutgo "
       + "WHERE IsTarget=1 AND IsTransfer=0 AND Date>='" +
       datefrom.strftime("%Y/%m/%d") + "'"
       + "And Account in (" + account_list + ")")
# print(sql)
df = pd.read_sql(sql, conn)
conn.close()

# https: // note.nkmk.me/python-pandas-datetime-timestamp/
# print(pd.to_datetime(df["Date"]))
df["Date"] = pd.to_datetime(df["Date"])
df['Year'] = df["Date"].dt.year
df['Month'] = df["Date"].dt.month

pd.set_option('display.max_rows', None)

start_of_nextmonth = basedate + relativedelta(months=1)
thismonth = df[(basedate <= df['Date']) & (df['Date'] < start_of_nextmonth)]
thismonth_sum = thismonth["Amount"].sum()
thismonth_expect = (thismonth_sum/date.today().day) * \
    mylib.get_end_of_month(basedate).day
# print(thismonth)

start_of_lastmonth = basedate + relativedelta(months=-1)
lastmonth = df[(start_of_lastmonth <= df['Date']) & (df['Date'] < basedate)]
lastmonth_sum = lastmonth["Amount"].sum()
# print(lastmonth)

start_of_lastyear = basedate + relativedelta(years=-1)
# print(start_of_lastyear)
last_one_year = df[(start_of_lastyear <= df['Date']) & (df['Date'] < basedate)]
last_one_year_mean = last_one_year.groupby(
    ['Year', 'Month']).sum()["Amount"].mean()

msg = "{year}年{month}月{day}日\n\n".format(
    year=date.today().year, month=date.today().month, day=date.today().day)
msg += '今月の使用確定額は {:,.0f}円 です。\n\n'.format(abs(thismonth_sum))
msg += '今月の予想使用額は {:,.0f}円 です。\n'.format(abs(thismonth_expect))
msg += '先月は {:,.0f} 円 でした。\n'.format(abs(lastmonth_sum))
msg += '過去1年間の平均は {:,.0f} 円 でした。\n'.format(abs(last_one_year_mean))

print(msg)
# https://api.slack.com/apps OAuth & Permissions
client = slack.WebClient(me_config["slack"]["token"])

response = client.chat_postMessage(
    channel=me_config["slack"]["channel"],
    text=msg)

# pt = pd.pivot_table(df, index=["Account", "Detail"], columns=[
#     "Year", "Month"], aggfunc='sum', values="Amount", fill_value="")
# pt.sort_values(by=["Account", "Detail"], inplace=True)

# # print(pt)
# html = pt.to_html()
# filename = os.path.join(me_config["workdir"], "report.html")
# with open(filename, mode="w", encoding='utf-8') as f:
#     f.write(html)

# ct = pd.crosstab(index=[df["Account"], df["Detail"]], columns=[
#     df["Year"], df["Month"]], values=df["Amount"], aggfunc='sum')
# # print(ct)
# # print(ct.columns)
# # print(ct[ct["Year"] == 2020])
# # browser.close()
