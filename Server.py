import socket
import threading


clients = []
msg = None


class ClientThread(threading.Thread):

    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port

    def run(self):
        while True:
            for cl in clients:
                try:
                    global msg
                    msg = cl.recv(1024).decode()
                except socket.error:
                    pass
                print(msg)
                if ' leave the group' in msg:
                    for client in clients:
                        try:
                            client.send(msg.encode())
                        except:
                            clients.remove(client)
                            break
                else:
                    for c in clients:
                        try:
                            c.send(msg.encode())
                        except:
                            clients.remove(c)


IP = socket.gethostbyname(socket.gethostname())
PORT = 8888

num_of_members = int(input("How many members you want in the group? "))


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen(num_of_members)
while num_of_members:
    conn, (ip, port) = server.accept()
    clients.append(conn)
    newThread = ClientThread(ip, port)
    newThread.start()
    num_of_members -= 1
server.close()

