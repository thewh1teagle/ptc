from client import Client
import curses
from ui import ChatUI
import random
import string

class Chat:
    def __init__(self) -> None:
        pass

    def _setup(self, stdscr):
        self.ui = ChatUI(stdscr)
        stdscr.clear()
        ui = ChatUI(stdscr)
        self.name = ui.wait_input("Username: ") # ''.join([random.choice('abcdefghijklmnop') for i in range(5)])# 
        host = ui.wait_input('Server host (empty for default): ') or 'localhost' # 'localhost'
        port = ui.wait_input('Server port (empty for default):') or '5555'
        self.client = Client(host, int(port), self.name)
        self.client.listen(self.message_handler)
        
        ui.userlist.append(self.name)
        ui.redraw_userlist()
    
    def setup(self):
        curses.wrapper(self._setup)

    def start(self):
        inp = ""
        while inp != "/quit":
            inp = self.ui.wait_input('>> ')
            self.client.send_text(inp)
            self.ui.chatbuffer_add(f' (You) {inp}')



    def message_handler(self, data: dict):
        # print(data)
        if data['type'] == 'new_user':
            self.ui.userlist.append(data['name'])
            self.ui.redraw_ui()
        if data['type'] == 'new_message':
            self.ui.chatbuffer_add(f' ({data["name"]}) {data["text"]}')
            self.ui.redraw_ui()
        if data['type'] == 'users_list':
            self.ui.userlist.clear()
            self.ui.userlist.append(f'{self.name} (You)')
            self.ui.userlist.extend(data['users'])
            self.ui.redraw_ui()

    