import socket
from _thread import *
from player import Player
import pickle
from score_manager import update_high_scores

server = "192.168.1.114"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

players = [Player(100,400), Player(900,400)]

Time_of_Round = 30  # время игры в секундах
Round_Timer = 120 * Time_of_Round
Game_Over = False
Reset_Timer = 300
pause = False

def threaded_client(conn, player):
    global Round_Timer, Game_Over, Reset_Timer, pause
    conn.send(pickle.dumps((players[player], Time_of_Round, Reset_Timer, pause)))
    reply = ""
    while True:
        try:
            data, p_pressed = pickle.loads(conn.recv(1024))
            players[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if p_pressed:
                    pause = not pause

                if player == 1:
                    reply = (players[0], Round_Timer, Game_Over, Reset_Timer, pause)
                else:
                    reply = (players[1], Round_Timer, Game_Over, Reset_Timer, pause)

                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))

            if not pause:

                # Обновление таймера и состояния игры
                if not Game_Over:
                    Round_Timer -= 1
                    if Round_Timer <= 0:
                        Game_Over = True
                        Reset_Timer = 300 # время респавна
                        #обновление результа
                        update_high_scores(max(players[0].Death_Count, players[1].Death_Count))
                        # print(max(players[0].Death_Count, players[1].Death_Count))

                else:
                    Reset_Timer -= 1
                    if Reset_Timer <= 0:
                        if Reset_Timer == 0 or Reset_Timer == 1 :
                            Game_Over = False
                        Round_Timer = 120 * Time_of_Round

        except:
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1