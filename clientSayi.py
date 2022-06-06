import sys
from networkSayi import Network
from PyQt5.QtWidgets import QApplication, QStackedWidget
from welcomeScreen import WelcomeScreen

def clearFiles():
    """
    oyuncuların tahmin ve puanlarını tutan 
    text dosyalarini yeni bir oyun için temizler
    """
    file1 = open("oyuncu1.txt", "w")
    file2 = open("oyuncu2.txt", "w")
    file1.write("")
    file2.write("")

    file1.close()
    file2.close()

def start():
    """
    yeni bir pencere yani client başlatır
    """

    clearFiles()
    
    n = Network()

    app = QApplication(sys.argv)
    widget = QStackedWidget()
    welcome = WelcomeScreen(widget, n, app)
    widget.addWidget(welcome)
    widget.setFixedWidth(800)
    widget.setFixedHeight(600)
    widget.show()

    player = int(n.getP())
    print(str(player) + ". oyuncusunuz")

    try:
        sys.exit(app.exec_())
    except:
        print("Program sonlandı!")
