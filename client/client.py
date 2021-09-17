import socket
import json
import threading
import time

class TcpSocket:

    def __init__(self, host, port) -> None:
        self.s = socket.socket()
        self.s.connect((host, port))
        self.on_new_message = None
        threading.Thread(target=self._listen).start()
    

    def send(self, data: dict):
        data = json.dumps(data)
        data = data.encode()
        # print(f'sending {data}')
        self.s.send(data)

    def _listen(self):
        while True:
            data = self.s.recv(1024)
            data = data.decode()
            data = json.loads(data)
            if self.on_new_message:
                self.on_new_message(data)

    def listen(self, message_handler: callable):
        self.on_new_message = message_handler


class Client:
    def __init__(self, host, port, name) -> None:
        self.s = TcpSocket(host, port)
        self._register(name)
        

    def _register(self, name):
        self.s.send({'type': 'register', 'name': name})

    def listen(self, message_handler):
        self.s.listen(message_handler)

    def send_text(self, text):
        self.s.send({'type': 'new_message', 'text': text})








