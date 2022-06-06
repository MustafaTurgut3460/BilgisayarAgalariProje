class Game:
   def __init__(self):
      self.p1Tahmin = False
      self.p2Tahmin = False
      self.p1Puan = False
      self.p2Puan = False
      self.p1Next = False
      self.p2Next = False
      self.ready = False
      self.tahminler = [None, None]
      self.puanlar = [None, None]
      self.tour = 1

   def getPlayerTahmin(self, p):
      """
      rakibin tahminini alır
      p: player id 0,1 -> int
      """
      if p == 0:
         return self.tahminler[1]
      else:
         return self.tahminler[0]

   def getPlayerPuan(self, p):
      """
      rakibin puanını alır
      p: player id 0,1 -> int
      """
      if p == 0:
         return self.puanlar[1]
      else:
         return self.puanlar[0]

   def nextTourIsReady(self):
      """
      sonraki tur hazır ise geçiş yapmak için değerleri ayarlar
      """
      return self.p1Next and self.p2Next

   def startNextRound(self, p):
      """
      ilgili oyuncunun sonraki tur için hazırlığını belirler
      p: player id 0,1 -> int
      """
      if p == 0:
         self.p1Next = True
      else:
         self.p2Next = True

      self.tour += 1


   def play(self, player, data):
      """
      player: player id 0,1 -> int
      data: tahmin veya puan değeri "12345" veya "++-" -> str
      gönderilen veriyi ilgili dataya aktarır ve hamleleri yapar
      """
      if str(data).startswith("t"):
         self.tahminler[player] = data[1:]
         if player == 0:
            self.p1Tahmin = True
         else:
            self.p2Tahmin = True
      else:
         self.puanlar[player] = data[1:]
         if player == 0:
            self.p1Puan = True
         else:
            self.p2Puan = True

   def connected(self):
      """
      oyunun hazır olup olmadığını kontrol eder
      """
      return self.ready

   def tahminlerHazirmi(self):
      return self.p1Tahmin and self.p2Tahmin

   def puanlarHazirmi(self):
      return self.p1Puan and self.p2Puan

   def reset(self):
      # oyunu resetler
      self.p1Tahmin = False
      self.p2Tahmin = False
      self.p1Puan = False
      self.p2Puan = False
      self.p1Next = False
      self.p2Next = False
      self.tour -= 2
      
      
