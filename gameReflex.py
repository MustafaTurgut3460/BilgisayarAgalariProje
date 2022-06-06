import random


class Game:
    def __init__(self):
        self.ready = False
        self.p1Shot = False
        self.p2Shot = False
        self.x = 0
        self.y = 0

    def getLocation(self):
        return self.x, self.y

    def connected(self):
        return self.ready

    def winner(self, p):
        if p == 0:
            self.p1Shot = True
        else:
            self.p2Shot = True

    def reset(self):
        self.p1Shot = False
        self.p2Shot = False
        self.x = 0
        self.y = 0

    def play(self):
        if self.x == 0:
            self.x = random.randint(0, 500)
        if self.y == 0:
            self.y = random.randint(0, 500)
