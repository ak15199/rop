__author__ = 'rafe'

import colorsys
import random


class Art(object):

    description = "Sleep drops"

    def __init__(self, matrix, config):
        self.drop_chance = config.get('DROP_CHANCE', 0.3)
        self.drop_speed = config.get('DROP_SPEED', (0.2, 0.4))
        self.fade = config.get('DROP_FADE', 0.95)

    def start(self, matrix):
        self.drops = []

    def refresh(self, matrix):
        matrix.fade(self.fade)
        delete = []
        for i, (x, y, (h, s, v), speed) in enumerate(self.drops):
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            r = int(r * 255)
            g = int(g * 255)
            b = int(b * 255)
            matrix.drawPixel(y, x, (r, g, b))
            v += speed
            if v > 1.0:
                v = 0.0
                y += 1
                if y > matrix.width:
                    delete.append(i)
            self.drops[i] = x, y, (h, s ,v), speed

        for i in reversed(delete):
            del self.drops[i]

        if random.random() <= self.drop_chance:
            x = random.randint(0, matrix.height)
            y = 0
            h, s, v = random.random(), 1.0, 0.0
            speed = random.uniform(*self.drop_speed)
            self.drops.append((x, y, (h, s, v), speed))

    def interval(self):
        return 30
