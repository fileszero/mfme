# -*- coding: utf-8 -*-

# https://selenium.dev/documentation/en/webdriver/driver_requirements/#firefox
# Simple assignment
import os
import json
import slack
import sys

from datetime import date
from datetime import datetime

from dateutil.relativedelta import relativedelta
import mylib
import sqlite3
import mfme_client

import glob
import pandas as pd  # pip install pandas


def updateIncomeOutgo(mfme: mfme_client, conn: sqlite3.Connection):
    mfme.updateLatestCSV()
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

    files = glob.glob(os.path.join(me_config["workdir"], "収入・支出詳細*.csv"))
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
    cur.close()


def updateBSHistory(mfme: mfme_client, conn: sqlite3.Connection):
    mfme.updateBSHistoryCSV()
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS BSHistory (
                Date datetime PRIMARY KEY,
                Total  INTEGER,
                Cash  INTEGER,
                Point  INTEGER
            ) """)

    files = glob.glob(os.path.join(me_config["workdir"], "資産推移月次.csv"))
    # print(files)
    for f in files:
        df = pd.read_csv(f, encoding="SHIFT-JIS")
        df.to_sql("import_work_bshist", conn, if_exists="replace")
        delete_sql = """
        DELETE FROM BSHistory WHERE Date IN (SELECT "日付" FROM import_work_bshist)
        """
        cur.execute(delete_sql)

        insetrt_sql = """
        INSERT INTO BSHistory(Date,Total,Cash,Point)
        SELECT "日付","合計（円）","預金・現金・仮想通貨（円）","ポイント（円）"
            FROM import_work_bshist
        """
        cur.execute(insetrt_sql)
        conn.commit()
        os.remove(f)
    cur.close()


def makeReportMessage(conn: sqlite3.Connection) -> str:
    basedate = datetime.combine(
        date.today().replace(day=1), datetime.min.time())
    # print(basedate)

    datefrom = basedate + relativedelta(months=-12)
    account_list = "'" + "','".join(me_config["mfme"]["reportAccount"]) + "'"
    sql = ("select * from IncomeOutgo "
           + "WHERE IsTarget=1 AND IsTransfer=0 AND Date>='" +
           datefrom.strftime("%Y/%m/%d") + "'"
           + "And Account in (" + account_list + ")")
    # print(sql)
    df = pd.read_sql(sql, conn)

    # https: // note.nkmk.me/python-pandas-datetime-timestamp/
    # print(pd.to_datetime(df["Date"]))
    df["Date"] = pd.to_datetime(df["Date"])
    df['Year'] = df["Date"].dt.year
    df['Month'] = df["Date"].dt.month

    pd.set_option('display.max_rows', None)

    start_of_nextmonth = basedate + relativedelta(months=1)
    thismonth = df[(basedate <= df['Date']) & (
        df['Date'] < start_of_nextmonth)]
    thismonth_sum = thismonth["Amount"].sum()
    thismonth_expect = (thismonth_sum/date.today().day) * \
        mylib.get_end_of_month(basedate).day
    # print(thismonth)

    start_of_lastmonth = basedate + relativedelta(months=-1)
    lastmonth = df[(start_of_lastmonth <= df['Date'])
                   & (df['Date'] < basedate)]
    lastmonth_sum = lastmonth["Amount"].sum()
    # print(lastmonth)

    start_of_lastyear = basedate + relativedelta(years=-1)
    # print(start_of_lastyear)
    last_one_year = df[(start_of_lastyear <= df['Date'])
                       & (df['Date'] < basedate)]
    last_one_year_mean = last_one_year.groupby(
        ['Year', 'Month']).sum()["Amount"].mean()

    msg = "{year}年{month}月{day}日\n\n".format(
        year=date.today().year, month=date.today().month, day=date.today().day)
    msg += '今月の確定額は {:>9,.0f} 円 です。\n\n'.format(abs(thismonth_sum))
    msg += '今月の予想額は {:>9,.0f} 円 です。\n'.format(abs(thismonth_expect))
    msg += '先月の確定額は {:>9,.0f} 円 でした。\n'.format(abs(lastmonth_sum))
    msg += '１年間の平均は {:>9,.0f} 円/月 です。\n'.format(abs(last_one_year_mean))

    return msg


def sendSlackMessage(msg: str):
    # print(msg)
    # https://api.slack.com/apps OAuth & Permissions
    client = slack.WebClient(me_config["slack"]["token"])

    client.chat_postMessage(
        channel=me_config["slack"]["channel"],
        text=msg)


me_config = mylib.get_config()

os.makedirs(me_config["workdir"], exist_ok=True)

mfme = mfme_client.mfme_client(me_config["mfme"])
if len(sys.argv) == 2:
    if sys.argv[1].startswith("https://moneyforward.com/users/two_step_verifications/verify"):
        mfme.MFAVerify(sys.argv[1])

conn = sqlite3.connect(me_config["dbfile"])
updateIncomeOutgo(mfme, conn)
updateBSHistory(mfme, conn)
msg = makeReportMessage(conn)
sendSlackMessage(msg)
conn.close()
