import json

class TcpSocket:
    def __init__(self, s) -> None:
        self.s = s
    
    def send(self, data: dict):
        data = json.dumps(data)
        data = data.encode()
        self.s.send(data)

    def get_update(self):
        data = self.s.recv(1024)
        data = data.decode()
        try:
            data = json.loads(data)
        except:
            pass
        return data

