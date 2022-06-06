import pygame
from networkRPS import Network
import pickle
pygame.font.init()

width = 800
height = 800


class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255,255,255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redrawWindow(win, game, p):
    win.fill((128,128,128))




    if not(game.connected()):
        image_hourglass = pygame.image.load(r"C:\Users\musta\Desktop\BilgisayarAgalariProje\hourglass-orange.png")
        win.blit(image_hourglass,(250,150))
        font = pygame.font.SysFont("comicsans", 60,True,True)
        text = font.render("Waiting for Player...", 1, (255,135,0))
        win.blit(text, (100,450))
    else:

        font = pygame.font.SysFont("comicsans", 60,True,True)
        text = font.render("Your Move Opponents", 1, (255, 135,0))
        win.blit(text, (80, 100))
        image_rock = pygame.image.load(r"C:\Users\musta\Desktop\BilgisayarAgalariProje\rock.png")
        image_paper = pygame.image.load(r"C:\Users\musta\Desktop\BilgisayarAgalariProje\paper.png")
        image_scissor = pygame.image.load(r"C:\Users\musta\Desktop\BilgisayarAgalariProje\scissors (1).png")

        win.blit(image_rock,(100,650))
        win.blit(image_scissor,(300,650))
        win.blit(image_paper,(525,650))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            text1 = font.render(move1, 1, (255,255,255))
            text2 = font.render(move2, 1, (255, 255, 255))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (255,255,255))
            elif game.p1Went:
                text1 = font.render("Locked In", 1, (255, 255, 255))
            else:
                text1 = font.render("Waiting...", 1, (255, 255, 255))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (255,255,255))
            elif game.p2Went:
                text2 = font.render("Locked In", 1, (255, 255, 255))
            else:
                text2 = font.render("Waiting...", 1, (255, 255, 255))

        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (425, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (425, 350))

        for btn in btns:
            btn.draw(win)

    pygame.display.update()





btns = [Button("Rock", 100, 525, (255,135,0)), Button("Scissors", 300, 525, (255,135,0)), Button("Paper", 500, 525, (255,135,0))]

def main(win):
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("comicsans", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You Won!", 1, (0,175,0))
            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, (100,50,50))
            else:
                text = font.render("You Lost...", 1, (175, 0, 0))

            win.blit(text, (175,200))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)

        redrawWindow(win, game, player)

def menu_screen():
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Rock Paper Scissors Game")
    run = True
    clock = pygame.time.Clock()
    image_rps=pygame.image.load(r"C:\Users\musta\Desktop\BilgisayarAgalariProje\rock-paper-scissors-ten.png")


    while run:


        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 60,True,True)
        win.blit(image_rps, (240, 250))
        text = font.render("Click to Play!", 1, (255,135,0))
        win.blit(text, (180,520))
        text1 = font.render("Rock Paper Scissors Game", 1, (255, 135, 0))
        win.blit(text1, (30, 150))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main(win)

def start():
    while True:
        menu_screen()