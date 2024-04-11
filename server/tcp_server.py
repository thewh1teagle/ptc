import threading
import socket
from client import Client
from tcp_socket import TcpSocket


class TcpServer:
    def __init__(self, host, port) -> None:
        self.s = socket.socket()
        self.host = host
        self.port = port
        self.s.bind((self.host, self.port))
        self.s.listen(5)
        self.clients = []



    def on_new_message(self, client: Client, data: dict):
        print(f'new message: {data}')
        if data['type'] == 'register':
            client.name = data['name']
            users = [i.name for i in self.clients if i.name != data['name']]
            client.socket.send({'type': 'users_list', 'users': users})
            self.broadcast_message({'type': 'new_user', 'name': data['name']}, exclude_name=data['name'])
        elif data['type'] == 'new_message':
            self.broadcast_message({'type': 'new_message', 'text': data['text'], 'name': client.name}, exclude_name=client.name)

    
    def broadcast_message(self, data, exclude_name = None):
        for client in self.clients:
            if exclude_name and exclude_name == client.name:
                continue
            client.socket.send(data)


    def connection(self, sock, addr):
        sock = TcpSocket(sock)
        client = Client(sock)
        self.clients.append(client)
        print(f'new Connection from {addr}')
        while True:
            data: dict = sock.get_update()
            self.on_new_message(client, data)

    def start(self):
        print(f'Server started on {self.host}:{self.port}...')
        while True:
            sock, addr = self.s.accept()
            threading.Thread(target=self.connection, args=(sock, addr,)).start()


