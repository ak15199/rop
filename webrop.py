from flask import Flask, Response, jsonify, request

import logging; logging.basicConfig(filename='web.log', level=logging.INFO)

import os.path
from random import seed
from time import sleep, time

from importer import ImportPlugins
from opc.matrix import OPCMatrix


# This code remains experimental. Configurtions are contained within the file.
M_WIDTH = 64
M_HEIGHT = 64

DFLT_FLIPTIME_SECS = 30

app = Flask(__name__)
app.config.from_object(__name__)


class Feed(object):

    def __init__(self):
        matrix = OPCMatrix(M_WIDTH, M_HEIGHT, "raw")
        arts = ImportPlugins("art", ["template.py"], [], matrix)
        if len(arts) == 0:
            matrix.terminate()
            print "Couldn't find any art to execute"
            exit(1)

        self.generator = self._frameGenerator(arts, matrix)
        self.packet = None

    def _frameGenerator(self, arts, matrix):
        while True:
            seed(time())

            for name, art in arts.iteritems():
                art.start(matrix)

                start_time = time()

                while time()-start_time < DFLT_FLIPTIME_SECS:
                    cycle_time = time()
                    art.refresh(matrix)
                    elapsed = time() - cycle_time
                    remaining = art.interval()/1000.0 - elapsed

                    yield {
                            "interval": remaining,
                            "expires": time()+remaining,
                            "data": matrix.show(),
                            }

    def _webHex(self, pix):
        return '{0:06x}'.format(((int(pix[0])*0x100) +
                                int(pix[1]))*0x100 + int(pix[2]))

    def produce(self):
        if self.packet is None or time() > self.packet["expires"]:
            frame = self.generator.next()
            data = [[self._webHex(pix) for pix in row] for row in frame["data"]]

            self.packet = {
                "interval": frame["interval"],
                "expires": frame["expires"],
                "data": data,
                }

        return self.packet


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


@app.route("/refresh.json")
def json_refresh():
    global feed

    return jsonify(feed.produce())


if __name__ == "__main__":
    global feed
    
    feed = Feed()

    app.run(threaded=True, debug=True)
