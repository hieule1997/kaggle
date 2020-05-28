
import time
import logging
import threading
from datetime import datetime

class Event(object):
    def __init__(self, desc, func, args=(), kwargs={}, use_thread=False):
        """
        desc: min hour day month dow
            day: 1 - num days
            month: 1 - 12
            dow: mon = 1, sun = 7
        """
        self.desc = desc 
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.use_thread = use_thread

    #support: 
    # * 
    # 59
    # 10,20,30
    def _match(self, value, expr):
        #print 'match', value, expr
        if expr == '*':
            return True
        values = expr.split(',')
        for v in values:
            if int(v) == value:
                return True
        return False

    def matchtime(self, t):
        mins, hour, day, month, dow = self.desc.split()
        return self._match(t.minute       , mins)  and\
               self._match(t.hour         , hour)  and\
               self._match(t.day          , day)   and\
               self._match(t.month        , month) and\
               self._match(t.isoweekday() , dow)

    def check(self, t):
        if self.matchtime(t):
            if self.use_thread:
                thread.start_new_thread(self.func, self.args, self.kwargs)
            else:
                try:
                    self.func(*self.args, **self.kwargs)
                except Exception as e:
                    logging.exception(e)

class Cron(object):
    def __init__(self):
        self.events = []

    def add(self, desc, func, args=(), kwargs={}, use_thread=False):
        self.events.append(Event(desc, func, args, kwargs, use_thread))

    def run(self):
        last_run = 0
        while True:
            #wait to a new minute start
            t = time.time()
            next_minute = t - t%60 + 60
            while t < next_minute:
                sleeptime = 60 - t%60
                logging.debug('current time: %s, we will sleep %.2f seconds' %(t, sleeptime))
                time.sleep(sleeptime)
                t = time.time()

            if last_run and next_minute - last_run != 60:
                logging.warn('Cron Ignored: last_run: %s, this_time:%s' % (last_run, next_minute) )
            last_run = next_minute

            current = datetime(*datetime.now().timetuple()[:5])
            for e in self.events:
                e.check(current)
            time.sleep(0.001)

def main2():
    def long_task():
        time.sleep(61)
        print ('long task ', time.time())
    #we will got warnning
    cron = Cron()
    cron.add('* * * * *'   , long_task) # every minute
    cron.run()

def main():
    def minute_task():
        print (time.time())
    def day_task():
        print (time.time())

    cron = Cron()
    cron.add('* * * * *'   , minute_task) # every minute
    cron.add('* * * * *'   , minute_task, use_thread=True) # every minute
    cron.run()

if __name__ == "__main__":
    main()