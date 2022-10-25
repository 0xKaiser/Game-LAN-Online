import socket
from _thread import *
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = '127.0.0.1'
port = 8000

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection")

currentId = "0"
listE = []
pos = ["0:100,500;0", "1:600,500;0"] # 
#scores = ['0:-3:0','1:-3:0']
def threaded_client(conn):
    global currentId, pos
    conn.send(str.encode(currentId))
    currentId = "1"
    reply = ''
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')
            if not data:
                conn.send(str.encode("Goodbye"))
                break

            id = int(reply.split(':')[0])
            if id == 0: nid = 1
            if id == 1: nid = 0

            if len(reply) <= 6: # position about Enemy 0:234
                print("Recieved Require E: " + reply)  
                if reply.split(':')[1] == '-2':
                    if len(listE) == 0:
                        
                        reply = str(nid) + ':' + '-5'
                        print('xac nhan listE rong')

                    if len(listE) > 0:
                        
                        countIdCoincide = 0
                        for enemy in listE:

                            if enemy.split(':')[0] != reply.split(':')[0]:
                                reply = str(enemy)
                                print('enemy tu server den ' + str(nid) + ' ' + reply)
                                listE.remove(enemy)
                                countIdCoincide +=1
                                break

                        if countIdCoincide == 0:
                            reply = str(nid) + ':' + '-5'
                            print('xac nhan listE toan bo id deu trung => rong')
    
                else:
                    listE.append(reply) 
                    reply = str(nid) + ':' + '-1'
                    print('da tao them gia tri moi trong listE')

                print("Sending: " + reply)

            if len(reply) >= 7:
                #print("Recieved: " + reply)
                pos[id] = reply # pos
                reply = pos[nid][:]
                #print("Sending: " + reply)

            conn.sendall(str.encode(reply))
        except:
            print('loi server')
            break

    print("Connection Closed")
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn,))