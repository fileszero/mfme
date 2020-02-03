# -*- coding: utf-8 -*-

import datetime
from dateutil.relativedelta import relativedelta

import test_mod1
import test_mod1_1

basedate = datetime.datetime.now().replace(day=1)
for m in range(3):
    curdate = basedate + relativedelta(months=-m)
    print(curdate.year)
    print(curdate.month)


print('[{:>9,.0f}]'.format(1234))
print('[{:>9,.0f}]'.format(12345))
print('[{:>9,.0f}]'.format(123456))
print('[{:>9,.0f}]'.format(1234567))
print('[{:>9,.0f}]'.format(12345678))
print('[{:>9,.0f}]'.format(123456789.01))

# UnicodeEncodeError: 'latin-1' codec can't encode characters in position 0-13: ordinal not in range(256)
# LC_CTYPE="C.UTF-8" python3 test.py
msg = '日本語プリントするとエラー？'
print(msg)
