import PyQt5
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QAction
from PyQt5 import uic, QtWidgets
import sys
import clientSayi, clientReflex, clientRPS

class MainMenu(QMainWindow):
    def __init__(self):
        super(MainMenu,self).__init__()

        # Ui dosyasını yükleme
        uic.loadUi("MainMenu.ui",self)

        # Widgetleri Tanımlama
        self.button_sayiTahmin = self.findChild(QPushButton, "pushButton_1")
        self.button_xox = self.findChild(QPushButton, "pushButton_2")
        self.button_tasKagitMakas = self.findChild(QPushButton, "pushButton_3")
        self.button_refleks = self.findChild(QPushButton, "pushButton_4")
        
        # Buton Tıklama
        self.button_sayiTahmin.clicked.connect(self.sayiTahminAc)
        self.button_xox.clicked.connect(self.xoxAc)
        self.button_tasKagitMakas.clicked.connect(self.tasKagitMakasAc)
        self.button_refleks.clicked.connect(self.refleksAc)

        self.show()

    

    def sayiTahminAc(self):
        clientSayi.start()


    def xoxAc(self):
        pass


    def tasKagitMakasAc(self):
        clientRPS.start() 


    def refleksAc(self):
        clientReflex.start()



app = QApplication(sys.argv)
menu = MainMenu()
menu.setWindowTitle("2 Kisilik Online Oyunlar")
menu.show()
app.exec_()