from exceptions import KeyboardInterrupt
from random import seed
import sys
from time import sleep, time
from traceback import format_exception

import dpyinfo
from importer import ImportPlugins
from opc.matrix import OPCMatrix
from opc.utils.prof import dumptimings

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

    sys.excepthook = exceptionHandler

    cycleCount = 0
    matrix = OPCMatrix(dpyinfo.WIDTH, dpyinfo.HEIGHT,
                        dpyinfo.ADDRESS, dpyinfo.ZIGZAG)
    arts = ImportPlugins("art", ["template.py"], sys.argv[1:], matrix)

    if len(arts) == 0:
        matrix.terminate()
        print "Couldn't find any art to execute"
        exit(1)

    while DFLT_CYCLE_COUNT is None or cycleCount < DFLT_CYCLE_COUNT:
        cycleCount += 1
        seed(time())

        for art in arts:
            matrix.setFirmwareConfig()
            art.start(matrix)
            t = time()
            while time()-t < DFLT_FLIPTIME_SECS:
                art.refresh(matrix)
                matrix.show()
                sleep(art.interval()/1000.0)

    matrix.terminate()


if __name__ == "__main__":
    main()
    dumptimings()
