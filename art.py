from __future__ import print_function

import logging
logging.basicConfig(filename='art.log', level=logging.DEBUG)

import argparse
from random import seed
import sys
if sys.version_info < (3,0,0):
    from exceptions import KeyboardInterrupt
from time import sleep, time
from traceback import format_exception

import config
from importer import ImportPlugins

from opc.colors import GRAY50, BLUE
from opc.error import TtyTooSmall
from opc.matrix import OPCMatrix
import opc.utils.prof as prof
from mwt import mwt

DFLT_FLIPTIME_SECS = 30
DFLT_CYCLE_COUNT = None

matrix = None


def matrixDone():
    global matrix
    if matrix is not None:
        try:
            matrix.clear()
            matrix.show()
        except TtyTooSmall:
            pass

        matrix.terminate()


def exceptionHandler(etype, evalue, etraceback):
    matrixDone()

    for line in format_exception(etype, evalue, etraceback):
        logging.error('Exception: '+line.rstrip('\n'))

    if etype is not KeyboardInterrupt:
        print("%s (see log for details)" % evalue)


def runart(art, name, args, matrix):
    if args.profile:
        logging.info("Start %s"%name)

    matrix.setFirmwareConfig()
    matrix.hq(False)
    matrix.clear()
    art.start(matrix)

    time_sound = 0  # sound as in 'sound as a pound'
    time_alarm = 0
    start_time = time()

    while time()-start_time < args.fliptime:
        cycle_time = time()
        art.refresh(matrix)
        matrix.show()

        # interval is between refreshes, but we take time to actually
        # render. Account for that here.
        debt_time = time()-cycle_time
        sleep_time = (art.interval()/1000.0) - debt_time
        if sleep_time > 0:
            sleep(sleep_time)
            time_sound += 1
        else:
            time_alarm += 1

    # timer overrun alarms are an indication that the art has higher
    # expectations of the hardware than is reasonable. If you see a
    # lot of these, then consider performance tuning, turning up the
    # art's interval, or buying better hardware
    pc_overrun = 100*time_alarm/(time_sound+time_alarm)
    if pc_overrun > 0:
        logging.info("%s: %d%% timer overrun alarms" % (name, pc_overrun))

    if args.profile:
        fmt = "%-25s %10s %10s %10s %10s"
        logging.info(fmt%("Cache", "Length", "Hits", "Misses", "Timeouts"))
        stats = mwt.stats()
        for stat in stats:
            logging.info(fmt%(stat["cache"], stat["length"], stat["hits"], stat["misses"], stat["timeouts"]))


@prof.timereference
def run(arts, args):
    global matrix

    cycleCount = 0

    while args.count is None or cycleCount < args.count:
        t=time()

        cycleCount += 1
        seed(time())

        for name, art in arts.iteritems():
            runart(art, name, args, matrix)


def _v(attr, default):
    try:
        return getattr(config, attr)
    except:
        return default


def progress(index, total):
    global matrix

    if total < 2:
        return

    matrix.clear()

    width = matrix.width-2
    offset = float(width*index)/total

    matrix.fillRect(1, matrix.midHeight-1, width, 2, GRAY50)
    matrix.fillRect(1, matrix.midHeight-1, offset, 2, BLUE)

    matrix.show()


def main():
    global matrix

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--count", type=int,
                        help="run for count cycles through all of the art",
                        default=DFLT_CYCLE_COUNT)
    parser.add_argument("-f", "--fliptime", type=int,
                        help="run art for FLIPTIME secs before transitioning",
                        default=DFLT_FLIPTIME_SECS)
    parser.add_argument("-p", "--profile",
                        help="switch on and report profiling detail",
                        action="store_true")
    parser.add_argument("art", help="Optional list of arts",
                        nargs="*")
    args = parser.parse_args()

    if args.profile:
        prof.on()

    matrix = OPCMatrix(
        _v("WIDTH", 16), _v("HEIGHT", 16),
        _v("DRIVER", "ansi"), _v("ZIGZAG", False),
        _v("FLIPUP", False), _v("FLIPLR", False)
        )

    arts = ImportPlugins("art", [], args.art, progress,
                         matrix, config.config)
    if len(arts) == 0:
        matrix.terminate()
        print("Couldn't find any art to execute")
        exit(1)

    run(arts, args)
    matrixDone()

    if args.profile:
        prof.dumptimings()


if __name__ == "__main__":
    sys.excepthook = exceptionHandler

    main()
