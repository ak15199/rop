from time import sleep, time
import dpyinfo
from opc.matrix import OPCMatrix
from random import seed
import sys
from importer import ImportPlugins

if __name__ == "__main__":
    FLIPTIME = 30

    matrix = OPCMatrix(dpyinfo.WIDTH, dpyinfo.HEIGHT, dpyinfo.ADDRESS, dpyinfo.ZIGZAG)
    arts = ImportPlugins("art", ["template.py"], sys.argv[1:], matrix)
    if len(arts) == 0:
        print "Couldn't find any art to execute"
        exit(1)

    while True:
        seed(time)

        for art in arts:
            matrix.setFirmwareConfig()
            art.start(matrix)
            t = time()
            while time()-t < FLIPTIME:
                art.refresh(matrix)
                matrix.show()
                sleep(art.interval()/1000.0)
                
