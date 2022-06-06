import time
from networkReflex import Network
import pygame

RED = (255, 0, 0)
LIGHT_BLUE = (153, 255, 255)
WHITE = (255, 255, 255)
WIDTH = 1000
HEIGHT = 600

pygame.init()
pygame.font.init()


class Client:
    """
    Sadece 1 oyuncu ekrana tıkladığında ekrana 'Diğer oyuncu bekleniyor' yazdırır
    2 oyuncu ekrana tıkladığında Start fonksiyonunu çağırır
    Parametre olarak Pencere ve Game classını alır
    """

    def drawWindow(self, win, game):
        win.fill(LIGHT_BLUE)
        if not (game.connected()):
            font = pygame.font.SysFont("comicsans", 60)
            text = font.render("Diğer oyuncu bekleniyor...", 1, RED)
            win.blit(
                text, (WIDTH / 2 - text.get_width() / 2, 130),
            )
            pygame.display.update()
        else:
            self.start()

    """
    Pygame ekranı oluşturur. while döngüsü içinde çalışır.
    Oyunculardan birisi balonu vurursa if koşuluna girer ve balonu 
    vuran oyuncunun ekranında 'Kazandınız!' diğer oyuncunun
    ekranındaysa 'Kaybettiniz!' yazdırır. 
    3 saniye delayden sonra drawWindow fonksiyonu çağrılır
    kullanıcılar çıkış yapana kadar oyun tekrar eder.
    """

    def main(self, win):
        run = True
        clock = pygame.time.Clock()
        self.n = Network()
        self.player = int(self.n.getPlayer())
        print(self.player, ". oyuncusunuz")

        while run:
            clock.tick(60)
            try:
                self.game = self.n.send("get")
            except:
                run = False
                print("Hata")
                break
            font = pygame.font.SysFont("comicsans", 150)
            if self.game.p1Shot or self.game.p2Shot:

                if (self.game.p1Shot and self.player == 0) or (
                    self.game.p2Shot and self.player == 1
                ):

                    text = font.render("Kazandınız!", 1, RED)
                else:
                    text = font.render("Kaybettiniz!", 1, RED)

                win.blit(
                    text, (WIDTH / 2 - text.get_width() / 2, 110,),
                )
                pygame.display.update()
                pygame.time.delay(3000)
                try:
                    self.game = self.n.send("reset")
                except:
                    run = False
                    break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

            self.drawWindow(win, self.game)

    """
    Oyunun gerçekleştiği fonksiyondur. Pygame'de oluşturulan ekranda
    3-2-1 şeklinde geri sayımdan sonra ekranın rastgele konumunda
    bir balon belirir. Mouse button down işlevinin gerçekleştiği
    konum alınır ve bu konum ile balonun konumu eşleşiyorsa
    vuran oyuncunun Shot sorgu değişkeni True olur ve döngüden çıkılır.  
    """

    def start(self):
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        screen.fill(WHITE)
        pygame.display.set_caption("Refleks Oyunu!")
        balloon = pygame.image.load("balloon.png")
        explode = pygame.image.load("explosion.png")
        a, b, c = (
            pygame.image.load("1.png"),
            pygame.image.load("2.png"),
            pygame.image.load("3.png"),
        )

        abc = (a, b, c)
        try:
            self.game = self.n.send("play")
        except Exception as e:
            print(e)
        rx, ry = self.game.getLocation()
        untilLastIndex = True
        while not (self.game.p1Shot or self.game.p2Shot):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if untilLastIndex:
                    for i in range(3):
                        screen.fill(WHITE)
                        screen.blit(abc[2 - i], [450, 50])
                        pygame.display.update()
                        time.sleep(1)
                        if i == 2:
                            screen.fill(WHITE)
                            location = screen.blit(balloon, (rx, ry))
                            pygame.display.update()
                            untilLastIndex = False
                            break
                self.game = self.n.send("get")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    posx = pos[0]
                    posy = pos[1]
                    if location.collidepoint(posx, posy):
                        screen.fill(WHITE)
                        screen.blit(explode, (rx, ry))
                        pygame.display.update()
                        try:
                            self.game = self.n.send("click")
                        except:
                            print("Hata")
                            break

    """
    Menü ekranını oluşturan fonksiyondur. Mouse button down
    işlevi ile fonksiyondan çıkılır ve main fonksiyonuna girilir.
    """

    def menuScreen(self):
        win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Refleks Oyunu")
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(60)
            win.fill(LIGHT_BLUE)
            font = pygame.font.SysFont("comicsans", 70)
            text = font.render("Oynamak için tıkla!", 1, RED)
            win.blit(text, (200, 200))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    run = False

        self.main(win)


def start():
    client = Client()
    while True:
        client.menuScreen()
