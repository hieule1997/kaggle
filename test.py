# import datetime

# date = datetime.datetime.now()
# threeWeeks = datetime.timedelta(weeks= 3)
# next_month = datetime.datetime(date.year + (date.month / 12), ((date.month % 12) + 1), 1)
# print (threeWeeks)
# print (next_month)


import datetime
import calendar

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)

somedate = datetime.date.today()

print(add_months(somedate,1))

