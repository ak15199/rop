import time
import logging

records = {}

class Record(object):

    def __init__(self, func):
        self.func = func
        self.times = []

    def addTime(self, t):
        self.times.append(t)

    def dump(self):
        logging.info("%20s %8d %8f %8f %8f %f" % (
            self.func,
            len(self.times),
            sum(self.times),
            min(self.times),
            sum(self.times)/len(self.times),
            max(self.times),
            ))

def dumptimings():
    global records

    logging.info("%d functions recorded", len(records))
    logging.info("%20s %8s %8s %8s %8s %s" % (
        "Function",
        "Count",
        "Tot Time",
        "Min",
        "Avg",
        "Max"
        ))

    for func, record in records.iteritems():
        record.dump()

def timefunc(f):
    def f_timer(*args, **kwargs):
        global records

        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        try:
            records[f.__name__].addTime(end-start)
        except:
            records[f.__name__] = Record(f.__name__)
            records[f.__name__].addTime(end-start)

        return result

    return f_timer
