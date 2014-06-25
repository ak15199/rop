from random import seed
import sys
from time import sleep, time

import dpyinfo
from importer import ImportPlugins
from opc.matrix import OPCMatrix

FLIPTIME = 30

if __name__ == "__main__":

    matrix = OPCMatrix(dpyinfo.WIDTH, dpyinfo.HEIGHT, dpyinfo.ADDRESS, dpyinfo.ZIGZAG)
    arts = ImportPlugins("art", ["template.py"], sys.argv[1:], matrix)
    if len(arts) == 0:
        print "Couldn't find any art to execute"
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
