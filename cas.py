# from crontab import CronTab
# from datetime import datetime

# def run():
#     print(datetime.now())
# # define the crontab for 25 minutes past the hour every hour
# entry = CronTab('* * * * *',run())

# while True:
#     entry.next()
# # find the delay from when this was run (around 11:13AM)
# # entry.next()
# # find the delay from when it was last scheduled
# # entry.next(datetime(2011, 7, 17, 11, 25))


import pycron
from datetime import datetime
import time
print(pycron.is_now('*/2 * * * *'))

while True:
    print(pycron.is_now('*/2 */2 * * *'))
    if pycron.is_now('*/5 */2 * * *'):
        print(datetime.now())
        # time.sleep(60)
    time.sleep(60)