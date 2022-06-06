import socket
from _thread import *
import pickle
from gameReflex import Game
import sys as sys

server = "192.168.1.108"
port = 15200

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(e)

s.listen(2)
print("Server başlatıldı, bağlantı bekleniyor")

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

            elif data == "click":
                game.winner(p)
            elif data == "reset":
                game.reset()
            elif data != "get":
                game.play()

            conn.sendall(pickle.dumps(game))
        except Exception as e:
            print(e)
            break

    print("Bağlantı kayboldu")

    try:
        del game
        print("Oyun sonlandırılıyor.")
        sys.exit()
    except:
        pass
    idCount -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print(str(addr) + "'e bağlanıldı")
    idCount += 1
    p = 0

    if idCount % 2 == 1:
        game = Game()
        print("Yeni oyun oluşturuluyor...")
    else:
        game.ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, game))
