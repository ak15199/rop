import argparse
from exceptions import KeyboardInterrupt
from random import seed
import sys
from time import sleep, time
from traceback import format_exception

import dpyinfo
from importer import ImportPlugins
from opc.matrix import OPCMatrix
import opc.utils.prof as prof

DFLT_FLIPTIME_SECS = 30
DFLT_CYCLE_COUNT = None

matrix = None

import logging; logging.basicConfig(filename='art.log', level=logging.DEBUG)


def exceptionHandler(etype, evalue, etraceback):
    global matrix
    if matrix is not None:
        matrix.terminate()

    for line in format_exception(etype, evalue, etraceback):
        logging.error('Exception: '+line.rstrip('\n'))

    if etype is not KeyboardInterrupt:
        print "%s (see log for details)" % evalue


def main():
    global matrix

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--count", type=int,
            help="run for count cycles through all of the art",
            default=DFLT_CYCLE_COUNT)
    parser.add_argument("-f", "--fliptime", type=int,
            help="run each art for fliptime seconds before transitioning to the next",
            default=DFLT_FLIPTIME_SECS)
    parser.add_argument("-p", "--profile",
            help="switch on and report profiling detail",
            action="store_true")
    parser.add_argument("art", help="Optional list of arts",
            nargs="*")
    args = parser.parse_args()

    if args.profile:
        prof.on()

    cycleCount = 0
    matrix = OPCMatrix(dpyinfo.WIDTH, dpyinfo.HEIGHT,
                        dpyinfo.ADDRESS, dpyinfo.ZIGZAG)

    arts = ImportPlugins("art", ["template.py"], args.art, matrix)
    if len(arts) == 0:
        matrix.terminate()
        print "Couldn't find any art to execute"
        exit(1)

    while args.count is None or cycleCount < args.count:
        cycleCount += 1
        seed(time())

        for art in arts:
            matrix.setFirmwareConfig()
            art.start(matrix)
            t = time()
            while time()-t < args.fliptime:
                art.refresh(matrix)
                matrix.show()
                sleep(art.interval()/1000.0)

    matrix.terminate()

    if args.profile:
        prof.dumptimings()


if __name__ == "__main__":
    sys.excepthook = exceptionHandler

    main()
