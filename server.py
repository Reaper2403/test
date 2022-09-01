import socket
import threading

host_name = "0.0.0.0"
port = 55555
host = socket.gethostbyname(host_name)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Sock stream is for TCP protocols
server.bind((host, port))
server.listen()

clients = []
nicknames = []


def broadcast(message, person):
    for client in clients:
        if person != nicknames[clients.index(client)]:
            client.send(message)


def handel_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message, nicknames[clients.index(client)])
        except:
            index = clients.index(client)
            clients.remove(client)
            nickname = nicknames[index]
            broadcast(f'{nickname} has left the chat'.encode('ascii'), nickname)
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
        broadcast(f'{nick} Joined the chat'.encode('ascii'), nick)
        client.send('Connected to the server'.encode('ascii'))
        thread = threading.Thread(target=handel_client, args=(client,))
        thread.start()


print(f"The server is listening....\n host: {host},\nport: {port}")
recieve()
