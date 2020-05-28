import croniter
import datetime

def shad():
    print(datetime.datetime.now())

cron = croniter.croniter('* */2 * * *', shad())
while True: 
    # cron = croniter.croniter('*/2 * * * *', shad())
    print(cron.get_next(datetime.datetime))
print(cron.get_next(datetime.datetime))
