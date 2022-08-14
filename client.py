import socket
import threading

client = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
client.connect(("2400:8904::f03c:93ff:fe97:a56e", 55555))
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

