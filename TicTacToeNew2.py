from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QAction
from PyQt5 import uic, QtWidgets
import sys
import threading
import socket


class MenuUI(QMainWindow):
    def __init__(self):
        super(MenuUI, self).__init__()

        # Ui dosyasını yükleme
        uic.loadUi("TicTacToeMenu.ui", self)

        # Widgetleri Tanımlama
        self.button_host = self.findChild(QPushButton, "button_host")
        self.button_connect = self.findChild(QPushButton, "button_connect")
        self.button_menu = self.findChild(QPushButton, "button_menu")

        # Buton Tıklama
        self.button_host.clicked.connect(self.host)
        self.button_connect.clicked.connect(self.connect)
        self.button_menu.clicked.connect(self.menu)
        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)
        self.show()

    def closeEvent(self, event):
        app.exit()

    def host(self):
        startServer()

    def connect(self):
        startClient()

    def menu(self):
        app.exit()


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # Ui dosyasını yükleme
        uic.loadUi("TicTacToe.ui", self)
        
        # Counter Tanımlama
        self.counter = 0
        self.turn = "X"
        self.you = "X"
        self.opponent = "O"
        self.gameOver = False
        self.loop1 = True

        # Widgetleri Tanımlama
        self.button1 = self.findChild(QPushButton, "button1")
        self.button2 = self.findChild(QPushButton, "button2")
        self.button3 = self.findChild(QPushButton, "button3")

        self.button4 = self.findChild(QPushButton, "button4")
        self.button5 = self.findChild(QPushButton, "button5")
        self.button6 = self.findChild(QPushButton, "button6")

        self.button7 = self.findChild(QPushButton, "button7")
        self.button8 = self.findChild(QPushButton, "button8")
        self.button9 = self.findChild(QPushButton, "button9")

        self.button10 = self.findChild(QPushButton, "button10")
        self.label1 = self.findChild(QLabel, "label1")

        # Buton Tıklama
        self.button1.clicked.connect(lambda: self.clicker(self.button1))
        self.button2.clicked.connect(lambda: self.clicker(self.button2))
        self.button3.clicked.connect(lambda: self.clicker(self.button3))

        self.button4.clicked.connect(lambda: self.clicker(self.button4))
        self.button5.clicked.connect(lambda: self.clicker(self.button5))
        self.button6.clicked.connect(lambda: self.clicker(self.button6))

        self.button7.clicked.connect(lambda: self.clicker(self.button7))
        self.button8.clicked.connect(lambda: self.clicker(self.button8))
        self.button9.clicked.connect(lambda: self.clicker(self.button9))

        self.button10.clicked.connect(self.quit_game)
        self.disable()
        self.label1.setText("Waiting Your Opponent!")

        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)
        self.show()

    def closeEvent(self, event):
        self.gameOver = True
        self.loop1 = False
        try:
            client.close()
        except:
            pass
        app.exit()

    def host_game(self, host, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        global client
        while self.loop1:
            try:
                server.settimeout(1)
                server.listen(1)
                client, addr = server.accept()
                if len(addr[0]) > 2:
                    self.loop1 = False
            except:
                pass
        try:
            #client, addr = server.accept()
            self.label1.setText("Your Turn!")
            self.you = "X"
            self.opponent = "O"
            global thread1
            thread1 = thread1 = threading.Thread(
                target=self.handleConnection, args=(client,)).start()
        except:
            pass
        server.close()

    def connect_to_game(self, host, port):
        global client
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while self.loop1:
            try:
                client.connect((host, port))
                self.label1.setText("Opponent Turn!")
                self.you = "O"
                self.opponent = "X"
                self.loop1 = False
                global thread1
                thread1 = thread1 = threading.Thread(
                    target=self.handleConnection, args=(client,)).start()
            except:
                self.label1.setText("Not Found Host!")

    def handleConnection(self, client):
        while not self.gameOver:
            if self.turn == self.you:
                self.enable()
            else:
                try:
                    data = client.recv(1024)
                    if not data:
                        break
                    else:
                        self.apply_move(data.decode('utf-8'))
                except:
                    self.label1.setText("Opponent Quit The Game!")
                    self.loop = False
                    self.gameOver = True
        client.close()

    def apply_move(self, data):
        button_list = [[self.button1, self.button2, self.button3],
                       [self.button4, self.button5, self.button6],
                       [self.button7, self.button8, self.button9]
                       ]

        b = button_list[int(data[0])][int(data[1])]
        b.setText(self.opponent)
        try:
            for i in range(3):
                for j in range(3):
                    if button_list[i][j].text() == self.you: 
                        button_list[i][j].setStyleSheet('color:rgb(0,255,0);background: rgb(234, 227, 0);border: 4px rgb(234, 227, 0);border-radius: 10px;')
                    elif button_list[i][j].text() == self.opponent:
                        button_list[i][j].setStyleSheet('color: rgb(255,0,0);background: rgb(234, 227, 0);border: 4px rgb(234, 227, 0);border-radius: 10px;')
        except:
            pass

        self.turn = self.you
        self.counter += 1
        self.label1.setText("Your Turn!")
        self.enable()
        self.checkWin()

    # Oyun Resetleme

    def quit_game(self):
        self.gameOver = True
        self.loop1 = False
        menu = MenuUI()
        widget.addWidget(menu)
        widget.setWindowTitle("Tic Tac Toe")
        widget.setCurrentIndex(widget.currentIndex()+1)
        widget.setFixedHeight(600)
        widget.setFixedWidth(800)
        try:
            client.close()
        except:
            pass

    # Kazanma Kontrol
    def checkWin(self):
        button_list = [[self.button1, self.button2, self.button3],
                       [self.button4, self.button5, self.button6],
                       [self.button7, self.button8, self.button9]
                       ]
        # Satır ve Sütun Kontrol
        for row in range(3):
            if button_list[row][0].text() == button_list[row][1].text() == button_list[row][2].text() != "":
                self.win(button_list[row][0],
                         button_list[row][1], button_list[row][2])
                return
        for col in range(3):
            if button_list[0][col].text() == button_list[1][col].text() == button_list[2][col].text() != "":
                self.win(button_list[0][col], button_list[1]
                         [col], button_list[2][col])
                return
        if button_list[0][0].text() == button_list[1][1].text() == button_list[2][2].text() != "":
            self.win(button_list[0][0], button_list[1][1], button_list[2][2])
        elif button_list[0][2].text() == button_list[1][1].text() == button_list[2][0].text() != "":
            self.win(button_list[0][2], button_list[1][1], button_list[2][0])
        elif self.counter == 9:
            self.tie()

    def button_gray(self, a, b, c):
        button_list = [self.button1, self.button2, self.button3,
                       self.button4, self.button5, self.button6,
                       self.button7, self.button8, self.button9
                       ]
        try:
            for d in button_list:
                if d == a or d == b or d == c:
                    pass
                else:
                    d.setStyleSheet('color:#797979;background: rgb(234, 227, 0);border: 4px rgb(234, 227, 0);border-radius: 10px;')
        except:
            pass


    def tie(self):
        a = self.button10
        self.button_gray(a, a, a)
        self.label1.setText("Tie Game!")
        self.disable()
        self.gameOver = True

    def win(self, a, b, c):
        self.gameOver = True
        if a.text() == self.you:
            self.button_gray(a, b, c),
            try:
                a.setStyleSheet('color: rgb(0,255,0);background: rgb(234, 227, 0);border: 4px rgb(234, 227, 0);border-radius: 10px;')
                b.setStyleSheet('color: rgb(0,255,0);background: rgb(234, 227, 0);border: 4px rgb(234, 227, 0);border-radius: 10px;')
                c.setStyleSheet('color: rgb(0,255,0);background: rgb(234, 227, 0);border: 4px rgb(234, 227, 0);border-radius: 10px;')
            except:
                pass
            self.label1.setText("You Win!")
            self.disable()
        else:
            self.button_gray(a, b, c)
            try:
                a.setStyleSheet('color: rgb(255,0,0);background: rgb(234, 227, 0);border: 4px rgb(234, 227, 0);border-radius: 10px;')
                b.setStyleSheet('color: rgb(255,0,0);background: rgb(234, 227, 0);border: 4px rgb(234, 227, 0);border-radius: 10px;')
                c.setStyleSheet('color: rgb(255,0,0);background: rgb(234, 227, 0);border: 4px rgb(234, 227, 0);border-radius: 10px;')
            except:
                pass
            self.label1.setText("You Lose!")
            self.disable()
        self.button10.setEnabled(True)

    # Tahtayı Kapatma
    def disable(self):
        button_list = [self.button1, self.button2, self.button3,
                       self.button4, self.button5, self.button6,
                       self.button7, self.button8, self.button9
                       ]

        for b in button_list:
            b.setEnabled(False)

    def enable(self):
        button_list = [self.button1, self.button2, self.button3,
                       self.button4, self.button5, self.button6,
                       self.button7, self.button8, self.button9
                       ]
        for b in button_list:
            if b.text() == "":
                b.setEnabled(True)

    # Buton Tıklama Fonksiyonu
    def clicker(self, b):
        b.setText(self.you)
        try:
            b.setStyleSheet('color: rgb(0,255,0);background: rgb(234, 227, 0);border: 4px rgb(234, 227, 0);border-radius: 10px;')
        except:
            pass
        button_list = [[self.button1, self.button2, self.button3],
                       [self.button4, self.button5, self.button6],
                       [self.button7, self.button8, self.button9]
                       ]
        for i in range(3):
            for j in range(3):
                if button_list[i][j] == b:
                    move = [i, j]
        self.turn = self.opponent
        data = str(move[0])+str(move[1])
        try:
            client.send(data.encode('utf-8'))
        except:
            self.label1.setText("Opponent Quit The Game!")
            self.loop = False
            self.gameOver = True
        self.counter += 1
        self.label1.setText("Opponent Turn!")
        self.disable()
        self.checkWin()


def startServer():
    xox = UI()
    widget.addWidget(xox)
    widget.setWindowTitle("Tic Tac Toe")
    widget.setCurrentIndex(widget.currentIndex()+1)
    widget.setFixedHeight(800)
    widget.setFixedWidth(600)
    global thread
    thread = threading.Thread(target=xox.host_game, args=(
        socket.gethostbyname(socket.gethostname()), 9967))
    thread.start()


def startClient():
    xox = UI()
    widget.addWidget(xox)
    widget.setWindowTitle("Tic Tac Toe")
    widget.setCurrentIndex(widget.currentIndex()+1)
    widget.setFixedHeight(800)
    widget.setFixedWidth(600)
    global thread
    thread = threading.Thread(target=xox.connect_to_game, args=(
        socket.gethostbyname(socket.gethostname()), 9967))
    thread.start()


def start():
    global app
    app = QApplication(sys.argv)
    global widget
    widget = QtWidgets.QStackedWidget()
    menu = MenuUI()
    widget.addWidget(menu)
    widget.setWindowTitle("Tic Tac Toe")
    widget.show()
    app.exec_()
