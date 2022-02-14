# we need to import a pair of libraries
import threading
import socket



# as i gonna run it on local machine there os localhost
host = '127.0.0.1'
# but also it could be specified automatically but be shure u don't use virtualbox
HOST = socket.gethostbyname(socket.gethostname())
# choose any free port, not reserved ports should be used
port = 55555
# specify used socket type for our server here TCP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# for undestanding for what socket gonna be used, here for hosting we should bind it to a host and a port
server.bind((host, port))
server.listen(5)

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            # cut off the failed client from our client list
            index = client.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break

def recieve():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))
        client.send('Connected to the server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print('Server is listening...')
recieve()



