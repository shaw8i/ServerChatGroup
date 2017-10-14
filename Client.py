import socket
import threading
import time


IP = socket.gethostbyname(socket.gethostname())
PORT = 8888

name = input("What's your name: ")


def recv_threading(client):
    while True:
        try:
            msg = (client.recv(1024).decode())
            print(msg)
        except:
            return

def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((IP, PORT))
    except:
        print("Error with connection")
        return
    client.send(('\n' + name + " join the group and his ip is '%s' \n" % IP).encode())

    recv_thread = threading.Thread(target=recv_threading, args=(client,))
    recv_thread.start()

    while True:
        time.sleep(0.5)
        msg = input()
        if msg == 'exit' or msg == 'quit':
            try:
                client.send((name + ' leave the group').encode())
                client.close()
                break
            except:
                print("connection lost!")
        else:
            try:
                client.send(('\n' + name + ': ' + msg).encode())
            except:
                print("connection lost!")
                break
def main():
    connect()


main()
