import socket
import threading


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("52.66.206.233", 55555))
nick = input('Enter your nickname please to enter the chat: ')

def recive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nick.encode('ascii'))
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break


def write():
    while True:
        message = f'{nick}: {input("")}'
        client.send(message.encode('ascii'))


recive_thread = threading.Thread(target=recive)
recive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

