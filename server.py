import socket
import threading

host_name = socket.gethostname()
port = 55555
tuple_IPV6=socket.getaddrinfo(host_name, port, socket.AF_INET6)
host = tuple_IPV6[0][1][0]


server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)  # Sock stream is for TCP protocols
server.bind((host, port))
server.listen()

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handel_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            nickname = nicknames[index]
            broadcast(f'{nickname} has left the chat'.encode('ascii'))
            nicknames.remove(nickname)
            break


def recieve():
    while True:
        client, address = server.accept()
        print(f'Connection established with {str(address)}')
        client.send('NICK'.encode('ascii'))
        nick = client.recv(1024).decode('ascii')
        clients.append(client)
        nicknames.append(nick)
        print(f"Nickname of the client is {nick}")
        broadcast(f'{nick} Joined the chat'.encode('ascii'))
        client.send('Connected to the server'.encode('ascii'))
        thread = threading.Thread(target=handel_client, args=(client,))
        thread.start()


print(f"The server is listening....\n host: {host},\nport: {port}")
recieve()
