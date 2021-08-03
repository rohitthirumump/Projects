import socket
from threading import Thread

host = '127.0.0.1'
port = 8080
client = {}
address = {}
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind((host,port))

def handle_clients(conn, address):
    name = conn.recv(1024).decode()
    welcome = "Welcome " +name+". You can type #quit if you ever want to leave the chat room"
    conn.send(bytes(welcome,'utf8'))
    msg = name+"Has joined the chat room"
    broadcast(bytes(msg,'utf8'))
    client[conn] = name

    while True:
        msg = conn.recv(1024)
        if msg != bytes('#quit','utf8'):
            broadcast(msg,name+":")
        else:
            conn.send(bytes('#quit','utf8'))
            conn.close()
            del client[conn]
            broadcast(bytes(name+"has left the chat room",'utf8'))

def accept_client_connection():
    while True:
        client_conn,client_address = sock.accept()
        print(client_address, "Has Connected")
        client_conn.send('Welcome to the Chat room, Please Type your name'.encode('utf8'))
        address[client_conn] = client_address

        Thread(target=handle_clients, args=(client_conn,client_address)).start()

def broadcast(msg,prefix = ''):
    for x in client:
        x.send(bytes(prefix,'utf8')+msg)

if __name__ == '__main__':
    sock.listen(5)
    print('The Server is running and is listening to clients request')

    t1 = Thread(target=accept_client_connection)
    t1.start()
    t1.join()


sock.close()