import logging
logging.basicConfig(filename='art.log', level=logging.DEBUG)

import argparse
from exceptions import KeyboardInterrupt
from random import seed
import sys
from time import sleep, time
from traceback import format_exception

import dpyinfo
from importer import ImportPlugins

from opc.error import TtyTooSmall
from opc.matrix import OPCMatrix
import opc.utils.prof as prof

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
        print "%s (see log for details)" % evalue


@prof.timereference
def run(arts, args):
    global matrix

    cycleCount = 0

    while args.count is None or cycleCount < args.count:
        cycleCount += 1
        seed(time())

        for name, art in arts.iteritems():
            matrix.setFirmwareConfig()
            matrix.hq(False)
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
                logging.info("%s: %d%% timer overrun alarms" %
                             (name, pc_overrun))


def _v(attr, default):
    try:
        return getattr(dpyinfo, attr)
    except:
        return default


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
        _v("ADDRESS", "ansi"), _v("ZIGZAG", False),
        _v("FLIPUP", False), _v("FLIPLR", False)
        )

    arts = ImportPlugins("art", [], args.art, matrix)
    if len(arts) == 0:
        matrix.terminate()
        print "Couldn't find any art to execute"
        exit(1)

    run(arts, args)
    matrixDone()

    if args.profile:
        prof.dumptimings()


if __name__ == "__main__":
    sys.excepthook = exceptionHandler

    main()
