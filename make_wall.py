__author__ = 'rafe'

import json

import config

layout = []

spacing = 0.15

for x in reversed(range(config.WIDTH)):
    for y in range(config.HEIGHT):
        xx = x - (config.WIDTH / 2)
        yy = y - (config.HEIGHT / 2)
        xx *= spacing
        yy *= spacing
        layout.append({'point': [yy, 0 , xx]})

print json.dumps(layout)
