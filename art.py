import curses
from random import seed
import sys
from time import sleep, time
from traceback import format_exception

import dpyinfo
from importer import ImportPlugins
from opc.matrix import OPCMatrix

FLIPTIME = 30

matrix = None

import logging; logging.basicConfig(filename='art.log',level=logging.DEBUG)

def exceptionHandler(type, value, tb):
    global matrix
    if matrix is not None:
        matrix.terminate()

    for line in format_exception(type, value, tb):
        logging.error('Exception: '+line.rstrip('\n'))

def main():
    global matrix

    sys.excepthook = exceptionHandler

    matrix = OPCMatrix(dpyinfo.WIDTH, dpyinfo.HEIGHT, dpyinfo.ADDRESS, dpyinfo.ZIGZAG)
    arts = ImportPlugins("art", ["template.py"], sys.argv[1:], matrix)

    if len(arts) == 0:
        logging.error("Couldn't find any art to execute")
        exit(1)

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
