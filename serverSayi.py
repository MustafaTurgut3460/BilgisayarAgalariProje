import socket
from _thread import *
import pickle
from gameSayi import Game

server = "192.168.1.108"
port = 5550

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(e)

s.listen(2)
print("Server başlatıldı, bağlantı bekleniyor...")

idCount = 0

def threaded_client(conn, p, game):
    global idCount
    conn.send(str.encode(str(p)))

    while True:
        try:
            data = conn.recv(4096).decode()
            print(data)

            if not data:
                break
            else:
                if data == "reset":
                    game.reset()

                elif data == "next":
                    game.startNextRound(p)

                elif data != "get":
                    game.play(p, data)

                conn.sendall(pickle.dumps(game))
                
        except:
            break

    print("Bağlantı kayboldu")

    try:
        del game
        print("Oyun sonlandiriliyor")
    except:
        pass

    idCount -= 1
    conn.close()

while True:
    conn, addr = s.accept()
    print(str(addr) + "'e bağlanıldı")

    idCount += 1
    p=0

    if idCount % 2 == 1:
        game = Game()
        print("Yeni oyun oluşturuluyor...")
    else:
        game.ready = True
        p=1

    start_new_thread(threaded_client, (conn, p, game))
