from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5 import QtGui

class GameScreen(QDialog):
   def __init__(self, network):
      self.n = network
      self.p = int(self.n.getP())
      super(GameScreen, self).__init__()
      loadUi("UI/Game.ui", self)
      self.waitingLabel.setVisible(False)

      self.oldT = str
      self.oldP = str

      # dosya yazim modlari
      self.TAHMIN_MODU = 't'
      self.PUAN_MODU = 'p'

      self.myNumberLabel.setText("Sayım: " + self.getNumber()) # kendi sayimizi gösterelim

      # click events
      self.sendButton.clicked.connect(self.send)
      self.nextRoundButton.clicked.connect(self.nextRound)

   def send(self):
      """
      Oyuncuların karşılıklı tahmin ve puanlarının gönderilmesini sağlar
      """
      if self.myPredictEdit.text() == "":
         # boş edittext
         self.showMessage("Lütfen bir tahmin/puan giriniz!", "Uyarı")
      else:
         if self.sendButton.text().startswith("T"):
            data = "t" + self.myPredictEdit.text()
            # tahmin gonder
            self.game = self.n.send(data)
            
            print(data)
            print("Tahmin Gönderildi!")

            # tahmini dosyaya yaz
            
            self.writeFile(data[1:], self.p, self.TAHMIN_MODU)

            if self.game.tahminlerHazirmi():
               self.sendButton.setText("Puan Gönder")
               print("Tahminler hazır")
               self.myPredictEdit.setText("")
               self.myPredictEdit.setPlaceholderText("Puanınızı Giriniz...")
               self.waitingLabel.setVisible(False)

               self.rakipPredictNumber.setText(self.game.getPlayerTahmin(self.p))

               self.showMessage("Tahminler Gönderildi!", "Uyarı")

            else:
               # tahminler hazir degil
               self.waitingLabel.setVisible(True)

         else:
            # puan gonder
            data = "p" + self.myPredictEdit.text()
            self.game = self.n.send(data)
            print("Puan Gönderildi!")

            self.writeFile(data[1:], self.p, self.PUAN_MODU)

            if self.game.puanlarHazirmi():
               print("Puanlar Hazır")
               self.rakipPoint.setText(self.game.getPlayerPuan(self.p))
               self.myPredictEdit.setText("")
               self.waitingLabel.setVisible(False)

               self.showMessage("Puanlar Gönderildi!", "Uyarı")

            else:
               #puanlar hazir degil henuz
               self.waitingLabel.setVisible(True)


   def nextRound(self):
      """
      Sonraki tur için gerekli kontrolleri yapar ve sonraki turu başlatır
      """
      if self.game.puanlarHazirmi():
         # bir sonraki tura gec
         self.game = self.n.send("next")
         print(self.game.p1Next, self.game.p2Next)

         if self.game.nextTourIsReady():
            # bütün herşeyi sıfırla ve diğer tura geç
            print("Sonraki tura geçiliyor...")
            self.game = self.n.send("reset")
            self.game = self.n.send("next") # aynı anda geçilemediği için bir çözüm
            self.sendButton.setText("Tahmin Gönder")
            self.rakipPredictNumber.setText("-----")
            self.rakipPoint.setText(".....")
            self.myPredictEdit.setPlaceholderText("Tahmininizi Giriniz...")
            self.tourLabel.setText(str(self.game.tour) + ". TUR")
            self.waitingLabel.setVisible(False)
            
            self.addItemToListview(self.p)

            self.showMessage("Bir sonraki tura geçildi!", "Uyarı")

         else:
            self.waitingLabel.setVisible(True)

      else:
         self.showMessage("Lütfen turu bitiriniz!", "Uyarı")


   def getNumber(self):
      file = open("myNumber.txt", "r")
      myNumber = file.read()
      file.close()

      return myNumber

   def writeFile(self, data, p, mode):
      """
      data: yazilacak veri -> str
      p: player id (0,1) -> int
      mode: tahmin ya da puan (t,p) -> char
      """
      if p == 0:
         # player 1 dosyasi acilacak
         file = open("oyuncu1.txt", "a")
      else:
         file = open("oyuncu2.txt", "a")

      if mode == 't':
         # tahmin modu ile acilacak
         if not self.oldT == data:
            file.write(data + " -> ")
            self.oldT = data
      elif mode == 'p':
         # puan modu ile acilacak
         if not self.oldP == data:
            file.write(data + "\n")
            self.oldP = data

      file.close()

   def readFile(self, fileName):
      """
      fileName: dosya ismi -> str
      return: okunan satirlarin listesi -> list
      """
      file = open(fileName, "r")
      liste = file.readlines()
      file.close()

      return liste

   def addItemToListview(self, p):
      """
      list: listeye eklenecek veriler -> list
      p: oyuncu id 0,1 -> int
      """
      list1 = self.readFile("oyuncu1.txt")
      list2 = self.readFile("oyuncu2.txt")

      self.myNumbersListview.clear()
      self.rakipNumbersListview.clear()

      if p == 0:
         # oyuncu 1 ekranı
         self.myNumbersListview.addItems(list1)
         self.rakipNumbersListview.addItems(list2)
      else:
         # oyuncu 2 ekranı
         self.myNumbersListview.addItems(list2)
         self.rakipNumbersListview.addItems(list1)

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
      