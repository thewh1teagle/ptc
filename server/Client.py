from tcp_socket import TcpSocket

class Client:
    def __init__(self, socket: TcpSocket, name: str = None) -> None:
        self.socket: TcpSocket = socket
        self.name = name
    