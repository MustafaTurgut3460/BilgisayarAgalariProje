import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from GameScreen import GameScreen

class WelcomeScreen(QDialog):
   def __init__(self, widget, network, app):
      self.n = network
      self.app = app
      self.widget = widget
      super(WelcomeScreen, self).__init__()
      loadUi("UI/WelcomeScreenUI.ui", self)
      self.searchLabel.setVisible(False)

      self.startButton.clicked.connect(self.startGame)

   def startGame(self):
      print("Start butonuna basıldı!")
      myNumber = self.myNumberEdit.text()

      if len(myNumber) == 0:
         self.showMessage("Oyuna başlamak için lütfen bir sayı belirleyiniz!", "Uyarı")

      else:
         # sayiyi dosyaya kaydet
         file = open("myNumber.txt", "w")
         file.write(myNumber)
         file.close()
         self.searchLabel.setVisible(True)
         self.startButton.setEnabled(False)
         self.exitButton.setEnabled(False)

         try:
            self.game = self.n.send("get")
         except:
            print("Oyun bulunamadı")
            self.app.exit()

         if self.game.connected():
            self.goToGameScreen()
      
   def goToGameScreen(self):
      gameScreen = GameScreen(self.n)
      self.widget.addWidget(gameScreen)
      self.widget.setCurrentIndex(self.widget.currentIndex()+1)

   def showMessage(self, message, title):
      """
      Uyarı mesaj penceresi gösterir
      message: gösterilecek mesaj -> str
      title: pencere başlığı -> str
      """
      msgBox = QMessageBox()
      msgBox.setWindowTitle(title)
      msgBox.setText(message)
      msgBox.setIcon(QMessageBox.Icon.Information)
      msgBox.setWindowIcon(QtGui.QIcon("Icon/information.png"))
      msgBox.exec_()
      

