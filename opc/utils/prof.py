import time
import logging
from functools import wraps

active = False
records = {}


class Record(object):

    def __init__(self, func, reference):
        self.reference = reference
        self.func = func
        self.times = []

    def addTime(self, t):
        self.times.append(t)

    def presentable(self):
        return len(self.times) > 0 and not self.reference

    def aggregate(self, totaltime):
        total = sum(self.times)
        return {
            "func": self.func,
            "count": len(self.times),
            "percent": 100.0/totaltime*total,
            "total": total,
            "min":  min(self.times),
            "avg":  sum(self.times)/len(self.times),
            "max":  max(self.times),
            }


def _dumptiming(result):
    logging.info("prof: %20s %8d %6.2f %8.4f %8.4f %8.4f %8.4f" % (
        result["func"],
        result["count"],
        result["percent"],
        result["total"],
        result["min"],
        result["avg"],
        result["max"],
        ))


def _totaltime():
    global records

    peak = 0
    for func, record in records.iteritems():
        try:
            peak = max(peak, sum(record.times))
        except:
            logging.info("except 1: %s %s" % (record.name, str(record.times)))

    return peak


def dumptimings():
    global records

    totaltime = _totaltime()

    results = [record.aggregate(totaltime) for record in records.values()
               if record.presentable()]

    logging.info("prof: %d functions recorded", len(results))
    logging.info("prof:")
    logging.info("prof: %20s %8s %6s %8s %8s %8s %8s" % (
        "Function",
        "Count",
        "% Time",
        "Tot Time",
        "Min",
        "Avg",
        "Max"
        ))

    rows = sorted(results, key=lambda record: record["percent"], reverse=True)
    for row in rows:
        _dumptiming(row)

    logging.info("prof:")


def on():
    global active
    active = True


def off():
    global active
    active = False


def timefunc(f, reference=False):
    global records

    records[f.__name__] = Record(f.__name__, reference)

    @wraps(f)
    def f_timer(*args, **kwargs):
        global active

        if not active:
            return f(*args, **kwargs)

        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()

        records[f.__name__].addTime(end-start)

        return result

    return f_timer


def timereference(f):
    return timefunc(f, True)
