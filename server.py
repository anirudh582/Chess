import socket
from _thread import *
import pickle

server = "10.10.10.109"
port = 1234 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

player_alliance=['W','B']
conns = {} 
def threaded_client(conn, player):
    conn.send(str.encode(player_alliance[player]))
    if player not in conns:
        conns[player_alliance[player]]=conn
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            print("Received: ", data)
            player_alliance_recv, init_sq, final_sq = data

            if not data:
                print("Disconnected")
                break
            else:
                if player_alliance_recv == 'W':
                    if 'B' in conns:
                        reply_conn = conns['B']
                        reply_conn.sendall(pickle.dumps(data))
                        print("Sending : ", data)
                elif player_alliance_recv == 'B':
                    if 'W' in conns:
                        reply_conn = conns['W']
                        reply_conn.sendall(pickle.dumps(data))
                        print("Sending : ", data)

        except:
            break

    print("Lost connection")
    conn.close()
        


currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    print(conns)
    start_new_thread(threaded_client, (conn, currentPlayer)) 

    currentPlayer += 1
