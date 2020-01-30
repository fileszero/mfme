import datetime
from dateutil.relativedelta import relativedelta

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
