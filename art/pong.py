from opc.colors import rgb

from random import randrange, random

WINTHRESH = 9


def coinToss():
    return random() >= .5


class Net(object):

    COLOR = rgb["gray30"]
    FREQ = 2               # on|off dash frequency

    def __init__(self):
        pass

    def display(self, matrix):
        for y in range(matrix.width):
            if ((1+y)/self.FREQ) % self.FREQ == 0:
                matrix.drawLine(matrix.width/2-1, y,
                                matrix.width/2, y, self.COLOR)


class Digit(object):

    # condensed numeric characters, with two rows of pixels
    # per byte in a 4x6 grid
    charmap = [
        (105, 153, 150),    # 0
        (38, 34, 39),       # 1
        (105, 18, 79),      # 2
        (105, 33, 150),     # 3
        (136, 170, 242),    # 4
        (248, 241, 150),    # 5
        (120, 233, 150),    # 6
        (241, 36, 68),      # 7
        (105, 105, 150),    # 8
        (105, 113, 22),     # 9
        ]

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def _draw(self, matrix, y, line):
        x = self.x
        while line > 0:
            if line & 1:
                matrix.drawPixel(x, y, self.color)
            line = line >> 1
            x -= 1

    def display(self, matrix, value):
        bytes = self.charmap[value]
        y = self.y
        for byte in bytes:
            self._draw(matrix, y-0, byte >> 4)
            self._draw(matrix, y-1, byte & 15)
            y -= 2


class Score(object):

    COLOR = rgb["red4"]

    def __init__(self, width, height, isLeft):
        if isLeft:
            x = width/2 - 3
        else:
            x = width/2 + 5

        y = height/2 + 2

        self.score = 0
        self.digit = Digit(x, y, self.COLOR)

    def reset(self):
        self.score = 0

    def goal(self):
        self.score += 1

    def wins(self, winthresh):
        return self.score >= winthresh

    def display(self, matrix):
        self.digit.display(matrix, self.score)


class Bat(object):

    COLOR = rgb["yellow"]
    RADIUS = 2              # half the size of the bat

    def __init__(self, width, height, isLeft):
        self.width = width
        self.height = height
        self.y = self.height/2 - self.RADIUS
        if isLeft:
            self.x = width - 1
        else:
            self.x = 0

    def up(self):
        self.y = min(self.y+1, self.height-self.RADIUS-1)

    def down(self):
        self.y = max(self.y-1, self.RADIUS)

    def display(self, matrix):
        matrix.drawLine(self.x, self.y-self.RADIUS,
                        self.x, self.y+self.RADIUS, self.COLOR)

    def intersects(self, x, y):
        return abs(x - self.x) == 1 and self.y-self.RADIUS < y \
            and y < self.y+self.RADIUS

    def behind(self, x, isLeft):
        if isLeft:
            if x <= 0:
                return True
        else:
            if x >= self.width:
                return True

        return False

    def _bounceDirection(self, ball_y):
        if ball_y > self.y:
            return -1
        elif ball_y < self.y:
            return 1

        if coinToss():
            return 1

        return -1

    def bounceAngle(self, ball_y):
        direction = self._bounceDirection(ball_y)

        if ball_y == self.y:
            return direction * random()

        return direction * abs(self.y-ball_y)


class Player(object):

    def __init__(self, width, height, isLeft):
        self.bat = Bat(width, height, isLeft)
        self.score = Score(width, height, isLeft)
        self.left = isLeft
        self.width = width

    def _mySide(self, ball_y):
        if self.left:
            if ball_y >= self.width/2:
                return True
        elif ball_y < self.width/2:
            return True

        return False

    def move(self, ball_x, ball_y):
        if (coinToss() and coinToss()) or not self._mySide(ball_x):
            return

        if ball_y > self.bat.y:
            self.bat.up()
        elif ball_y < self.bat.y:
            self.bat.down()

    def opponent(self):
        return not self.left

    def ballIntersectsBat(self, ball_x, ball_y):
        return self.bat.intersects(ball_x, ball_y)

    def ballIntersectsWall(self, ball_x, ball_y):
        return self.bat.behind(ball_x, self.left)

    def bounceAngle(self, ball_x, ball_y):
        return self.bat.bounceAngle(ball_y)

    def display(self, matrix):
        self.bat.display(matrix)
        self.score.display(matrix)


class Ball(object):

    SERVEMARGIN = 4

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def serve(self, serveFromLeft, y=None):
        if y is None:
            self.y = randrange(self.SERVEMARGIN, self.height-self.SERVEMARGIN)
        else:
            self.y = y

        if serveFromLeft:
            self.x = self.SERVEMARGIN
            self.h = 1
        else:
            self.x = self.width-self.SERVEMARGIN
            self.h = -1

        if coinToss():
            self.v = randrange(1, 2)
        else:
            self.v = -randrange(1, 2)

    def bounce(self, acceleration):
        self.h = -self.h
        self.v = acceleration

    def move(self):
        self.x += self.h
        self.y += self.v

        # take into account bouncing off top or bottom while the
        # ball is in flight
        if self.y <= 0:
            self.v = abs(self.v)
        elif self.y >= self.height-1:
            self.v = -abs(self.v)

    def display(self, matrix):
        matrix.drawPixel(self.x, self.y, rgb["white"])


class Art(object):

    description = "Automated pong"

    def __init__(self, matrix):
        self.ball = Ball(matrix.width, matrix.height)
        self.net = Net()

        self.players = {}
        for left in [True, False]:
            self.players[left] = Player(matrix.width, matrix.height, left)

        self._newGame()

    def start(self, matrix):
        matrix.setFirmwareConfig(nointerp=True)

    def _newGame(self):
        for player in self.players.values():
            player.score.reset()

        self.ball.serve(coinToss())

    def refresh(self, matrix):

        for player in self.players.values():
            opponent = self.players[player.opponent()]
            if opponent.score.wins(WINTHRESH):
                self._newGame()

            player.move(self.ball.x, self.ball.y)
            if player.ballIntersectsBat(self.ball.x, self.ball.y):
                bounceAngle = player.bounceAngle(self.ball.x, self.ball.y)
                self.ball.bounce(bounceAngle)
            elif player.ballIntersectsWall(self.ball.x, self.ball.y):
                opponent.score.goal()
                self.ball.serve(player.left, player.bat.y)

        self.ball.move()
        matrix.clear()

        for player in self.players.values():
            player.display(matrix)

        self.net.display(matrix)
        self.ball.display(matrix)

    def interval(self):
        return 140
