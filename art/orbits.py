from _baseclass import ArtBaseClass

from opc.colors import YELLOW, GRAY50, RY2, BLUE
from math import sin, cos, atan2, sqrt


"""
Based on https://fiftyexamples.readthedocs.org/en/latest/gravity.html
"""


def k(dist):
    return 1000*dist


def au(dist):
    return AU*dist


G = 6.67428e-11
AU = k(149.6e6)     # 149.6 million km, in meters.


class Body(object):

    """
    mass : mass in kg
    vx, vy: x, y velocities in m/s
    px, py: x, y positions in m
    """

    def __init__(self, name, mass, color, vx=0.0, vy=0.0, px=0.0, py=0.0):
        self.name = name
        self.mass = mass
        self.color = color
        self.vx, self.vy = vx, vy
        self.px, self.py = px, py

    def attraction(self, other):
        # Compute the distance of the other body.
        sx, sy = self.px, self.py
        ox, oy = other.px, other.py
        dx = (ox-sx)
        dy = (oy-sy)
        d = sqrt(dx**2 + dy**2)

        # Report an error if the distance is zero; otherwise we'll
        # get a ZeroDivisionError exception further down.
        if d == 0:
            raise ValueError("Collision between objects %r and %r" %
                             (self.name, other.name))

        # Compute the force of attraction
        f = G * self.mass * other.mass / (d**2)

        # Compute the direction of the force.
        theta = atan2(dy, dx)
        fx = cos(theta) * f
        fy = sin(theta) * f

        return fx, fy

    def update(self, force, timestep):
        fx, fy = force
        self.vx += fx / self.mass * timestep
        self.vy += fy / self.mass * timestep

        self.px += self.vx * timestep
        self.py += self.vy * timestep

    def draw(self, matrix, cx, cy, scale):
        matrix.drawPixel(cx+self.px*scale, cx+self.py*scale, self.color)


class Simulation(object):

    def __init__(self):
        self.timestep = 24*3600  # One day
        self.bodies = [
            Body("Sun",     1.9889e30, YELLOW),
            Body("Mercury", 3.3022e23, GRAY50, px=au(.4),   vy=k(-47.362)),
            Body("Venus",   4.8685e24, RY2,    px=au(.723), vy=k(-35.02)),
            Body("Earth",   5.9742e24, BLUE,   px=au(-1),   vy=k(29.783)),
            ]

    def clock(self, matrix, cx, cy, scale):
        force = {}
        for body in self.bodies:
            # Add up all of the forces exerted on 'body'.
            total_fx = total_fy = 0.0
            for other in self.bodies:
                # Don't calculate the body's attraction to itself
                if body is not other:
                    fx, fy = body.attraction(other)
                    total_fx += fx
                    total_fy += fy

            # Record the total force exerted.
            force[body] = (total_fx, total_fy)

        # Update velocities based on the force, and draw.
        for body in self.bodies:
            body.update(force[body], self.timestep)
            body.draw(matrix, cx, cy, scale)


class Art(ArtBaseClass):

    description = "Simulate orbit of Mercury, Venus, and Earth"

    def __init__(self, matrix):
        self.scale = min(matrix.width, matrix.height) / (2 * AU)
        self.cx, self.cy = matrix.width/2.0, matrix.height/2.0
        self.simulation = Simulation()

    def start(self, matrix):
        matrix.clear()

    def refresh(self, matrix):
        matrix.fade(0.99)
        self.simulation.clock(matrix, self.cx, self.cy, self.scale)

    def interval(self):
        return 10
