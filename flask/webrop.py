from __future__ import print_function

import os.path
from flask import Flask, Response, jsonify

import logging
logging.basicConfig(filename='art.log', level=logging.DEBUG)

import opc.utils.prof as prof

from random import seed
import sys
from time import sleep, time

import dpyinfo
from importer import ImportPlugins
from opc.matrix import OPCMatrix

M_WIDTH = 64
M_HEIGHT = 64

DFLT_FLIPTIME_SECS = 30

frameGenerator = None

app = Flask(__name__)
app.config.from_object(__name__)


def webHex(pix):
    return '{0:06x}'.format(((int(pix[0])*0x100) + int(pix[1]))*0x100 + int(pix[2]))


def convertToWebHex(data):
    packet = {
      "data": [ [ webHex(pix) for pix in row ] for row in data ] 
    }

    return packet


@app.route("/refresh.json")
def json_refresh():
    hexdata = convertToWebHex(next(generator))
    return jsonify(hexdata)


def frameGenerator(arts, matrix):
    cycleCount = 0

    while True:
        cycleCount += 1
        seed(time())

        for name, art in arts.items():
            matrix.setFirmwareConfig()
            art.start(matrix)

            time_sound = 0  # sound as in 'sound as a pound'
            time_alarm = 0
            start_time = time()

            while time()-start_time < DFLT_FLIPTIME_SECS:
                cycle_time = time()
                art.refresh(matrix)

                yield matrix.show()

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


def initialize():
    global generator

    matrix = OPCMatrix(M_WIDTH, M_HEIGHT, "raw")

    arts = ImportPlugins("art", ["template.py"], [], matrix)
    if len(arts) == 0:
        matrix.terminate()
        print("Couldn't find any art to execute")
        exit(1)

    generator = frameGenerator(arts, matrix)


def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))


def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(root_dir(), filename)
        return open(src).read()
    except IOError as exc:
        return str(exc)


@app.route('/', methods=['GET'])
def docroot():
    content = get_file('index.html')
    return Response(content, mimetype="text/html")


@app.route("/initialize.json")
def json_initialize():
    packet = {
          "xrange": M_WIDTH,
          "yrange": M_HEIGHT,
        }

    return jsonify(packet)


if __name__ == "__main__":
    initialize()
    app.run(threaded=True)

