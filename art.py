from random import seed
import sys
from time import sleep, time
from traceback import format_exception

import dpyinfo
from importer import ImportPlugins
from opc.matrix import OPCMatrix
from opc.error import TtyTooSmall

FLIPTIME = 30

matrix = None

import logging; logging.basicConfig(filename='art.log', level=logging.DEBUG)


def exceptionHandler(etype, evalue, etraceback):
    global matrix
    if matrix is not None:
        matrix.terminate()

    for line in format_exception(etype, evalue, etraceback):
        logging.error('Exception: '+line.rstrip('\n'))

    if type(etype) is type(TtyTooSmall):
        print "%s (see log for details)" % evalue

def main():
    global matrix

    sys.excepthook = exceptionHandler

    matrix = OPCMatrix(dpyinfo.WIDTH, dpyinfo.HEIGHT,
                        dpyinfo.ADDRESS, dpyinfo.ZIGZAG)
    arts = ImportPlugins("art", ["template.py"], sys.argv[1:], matrix)

    if len(arts) == 0:
        logging.error("Couldn't find any art to execute")
        exit(1)

    sleep(3)

    while True:
        seed(time())

        for art in arts:
            matrix.setFirmwareConfig()
            art.start(matrix)
            t = time()
            while time()-t < FLIPTIME:
                art.refresh(matrix)
                matrix.show()
                sleep(art.interval()/1000.0)

if __name__ == "__main__":
    main()
