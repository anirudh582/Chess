import socket
from _thread import *
import pickle

server = ""
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
currentPlayer = 0
def threaded_client(conn, player):
    conn.send(str.encode(player_alliance[player%2]))
    conns[player_alliance[player%2]]=conn
    global currentPlayer
    if currentPlayer<2:
        print("sending not ready")
        for _,conn in conns.items():
            conn.send(str.encode("not ready"))
    else:
        print("sending ready")
        for _,conn in conns.items():
            conn.send(str.encode("ready"))

    while True:
        try:
            print("ready to receive data for {}".format(player_alliance[player]))
            data = pickle.loads(conn.recv(2048))
            print("Received: ", data)
            player_alliance_recv, init_sq, final_sq, _= data

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

    if len(conns)>0:
        try:
            for key in conns.keys():
                del conns[key]
        except:
            pass
    currentPlayer=0
    print("Lost connection: ", player_alliance[player%2])
    conn.close()
        

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn, currentPlayer)) 
   
    currentPlayer += 1
