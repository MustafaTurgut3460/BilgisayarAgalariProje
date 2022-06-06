import pygame
from networkRPS import Network

width = 500
height = 500
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

clientNumber = 0
background = (27, 79, 114)
white = (236, 240, 241)
green = (0, 128, 0)
darkGreen = (0, 100, 0)
red = (231, 76, 60)
darkRed = (241, 148, 138)
darkBlue = (40, 116, 166)


class Player():
    def __init__(self, x, y, width, height, color,darkColor):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.darkColor=darkColor
        self.rect = (x,y,width,height)
        self.history = [[self.x, self.y]]
        self.vel = 3
        self.length = 1


    def draw(self):
        for i in range(len(self.history)):
            if i == self.length - 1:
                pygame.draw.rect(display, self.darkColor, (self.history[i][0], self.history[i][1], self.w, self.h))
            else:
                pygame.draw.rect(display, self.color, (self.history[i][0], self.history[i][1], self.w, self.h))

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            self.x += self.vel

        if keys[pygame.K_UP]:
            self.y -= self.vel

        if keys[pygame.K_DOWN]:
            self.y += self.vel

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)


def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


def redrawWindow(win,player, player2):
    win.fill((255,255,255))
    player.draw(win)
    player2.draw(win)
    pygame.display.update()


def main():
    run = True
    n = Network()
    startPos = read_pos(n.getP())
    p = Player(startPos[0],startPos[1],100,100,(0,255,0),darkRed)
    p2 = Player(0,0,100,100,(255,0,0),darkGreen)
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        p2Pos = read_pos(n.send(make_pos((p.x, p.y))))
        p2.x = p2Pos[0]
        p2.y = p2Pos[1]
        p2.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move()
        redrawWindow(display, p, p2)

def start():
    main()