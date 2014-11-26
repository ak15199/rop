import time
import logging

records = {}

class Record(object):

    def __init__(self, func):
        self.func = func
        self.times = []

    def addTime(self, t):
        self.times.append(t)

    def aggregate(self):
        return {
                "func": self.func,
                "count": len(self.times),
                "total": sum(self.times),
                "min":  min(self.times),
                "avg":  sum(self.times)/len(self.times),
                "max":  max(self.times),
            }


def dumptiming(result):
    logging.info("prof: %20s %8d %8f %8f %8f %f" % (
        result["func"],
        result["count"],
        result["total"],
        result["min"],
        result["avg"],
        result["max"],
        ))

def dumptimings():
    global records

    logging.info("prof: %d functions recorded", len(records))
    logging.info("prof:")
    logging.info("prof: %20s %8s %8s %8s %8s %s" % (
        "Function",
        "Count",
        "Tot Time",
        "Min",
        "Avg",
        "Max"
        ))

    results = []
    for func, record in records.iteritems():
        results.append(record.aggregate())

    for result in sorted(results, key=lambda record: record["total"], reverse=True):
        dumptiming(result)

active = False


def on():
    global active
    active = True


def off():
    global active
    active = False


def timefunc(f):

    def f_timer(*args, **kwargs):
        global active
        global records

        if not active:
            return f(*args, **kwargs)

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
