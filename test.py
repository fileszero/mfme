import datetime
from dateutil.relativedelta import relativedelta

basedate = datetime.datetime.now().replace(day=1)
for m in range(3):
    curdate = basedate + relativedelta(months=-m)
    print(curdate.year)
    print(curdate.month)
