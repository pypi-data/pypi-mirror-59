import socket
from time import sleep


from .log import Log
# from .bridge import Bridge
from threading import Thread
from .message import RawMessage


from .messageparser import parse_line


class Socket(Thread):
    
    # bridge: Bridge
    socket: socket.socket
    buffer: str
    active: bool
    ready: bool
    channel_list: list
    log: Log


    # def __init__(self, bridge: Bridge = None):
    def __init__(self, nick: str, token: str, verbose=False):
        # self.bridge = bridge
        Thread.__init__(self)
        self.nick = nick
        self.token = token
        self.active = True
        self.verbose = verbose
        self.buffer = ""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.channel_list = []
        
        

    def __connect(self):
        self.socket.connect(("irc.chat.twitch.tv", 6667))
        self._send_raw(f"PASS {self.token}")
        self._send_raw(f"NICK {self.nick}")
        self._send_raw("CAP REQ :twitch.tv/membership")
        self._send_raw("CAP REQ :twitch.tv/tags")
        self._send_raw("CAP REQ :twitch.tv/commands")
        pass

    def disconnect(self):
        if self.verbose:
            print("departing channels")
        for channel in self.channel_list:
            self._send_raw("PART #"+ channel.name.lower() +" ")
        try:
            self.socket.close()
        except Exception:
            pass

    def reconnect(self):
        if self.verbose:
            print("Reconnect detected!")
        self.disconnect()
        if self.verbose:
            print("Waiting to reconnect.")
        sleep(10)
        self.activate(self.channel_list)

    def connect_to_channel(self, channel: str):
        self._send_raw("JOIN #"+ channel.lower() +" ")
        # self.channel_list.append(channel)
        if self.verbose:
            print(f"connecting to '{channel}'")

    def disconnect_from_channel(self, channel: str):
        self._send_raw("PART #"+ channel.lower() +" ")
        # self.__clearchannel(channel)
        if self.verbose:
            print(f"departing from '{channel}'")

    def __clearchannel(self, channel: str):
        counter = 0
        for chn in self.channel_list:
            if chn.name == channel:
                self.channel_list.pop(counter)
                return
            counter += 1

    def activate(self, channels):
        self.channel_list = channels
        self.__connect()
        for channel in self.channel_list:
            self._send_raw("JOIN #"+ channel.name.lower() +" ")

    def run(self):
        while self.active:
            self.__process_stream_data()
            sleep(0.00001)
        try:
            self.socket.close()
        except Exception:
            pass

    def close(self):
        if self.verbose:
            print(f"({self.name}) Closing Socket")
        self.active = False
        self.socket.close()
        


    def _send_raw(self, message: str):
        try:
            self.socket.send((f"{message}\r\n").encode('utf-8'))
            if self.verbose:
                if message[:4] == "PASS":
                    print(f"({self.name}) < PASS ****")
                else:
                    print(f"({self.name}) < {message}")
        except OSError:
            self.log.error(f"Socket is closed and must be reopened to send the message '{message}'")

    def __process_stream_data(self):
        try:
            self.buffer = self.buffer + self.socket.recv(1024).decode()
        except ConnectionAbortedError:
            self.log.info("Socket connection has Closed")
        temp = self.buffer.split("\n")
        self.buffer = temp.pop()
        for line in temp:
            
            if ("PING :tmi.twitch.tv" in line): # Keep Alive Mechanism
                self._send_raw("PONG :tmi.twitch.tv")
            self.on_socket_data(line)


    def on_socket_data(self, line: str):
        raise NotImplementedError("`on_socket_data` not implemented")






class ReadSocket(Socket):

    def __init__(self, nick: str, token: str):
        Socket.__init__(self, nick, token)
        self.name = "Thread-ReadSocket"
        self.log = Log("ReadSocket")



    def on_socket_data(self, line: str):
        self.on_data(parse_line(line))

    def on_data(self, data):
        # print(f" >", data.line)
        for channel in self.channel_list:
            channel.on_raw(data)
        
        if data.inner == "Message":
            print(f"Message: {data.message}")
            for channel in self.channel_list:
                if channel.name in data.line:
                    channel.on_message(data)
        elif data.inner == "Join":
            for channel in self.channel_list:
                if channel.name in data.line:
                    channel.on_join(data)
        elif data.inner == "PrivateMessage":
            if data.display_name.lower() != self.nick.lower():
                for channel in self.channel_list:
                    if channel.name == data.channel:
                        self.log.chat(data.message_text, data.channel, data.display_name)
                        channel.on_privmessage(data)
        elif data.inner == "CommandMessage":
            if data.display_name.lower() != self.nick.lower():
                for channel in self.channel_list:
                    if channel.name == data.channel:
                        self.log.chat(f"[CMD] {data.message_text}",data.channel, data.display_name)
                        channel.on_command(data) 
    

class SendSocket(Socket):

    def __init__(self, nick: str, token: str):
        Socket.__init__(self, nick, token)
        self.name = "Thread-SendSocket"
        self.log = Log("SendSocket")

    def join(self, channel: str):
        send = f"JOIN #{channel.lower()}"
        self._send_raw(send)

    def send_message(self, channel: str, message: str):
        send = f"PRIVMSG #{channel.lower()} :{message}"
        self._send_raw(send)
        self.log.sent(message, channel.lower())
    
    def send_action_message(self, channel: str, message: str):
        send = f"PRIVMSG #{channel.lower()} :/me {message}"
        self._send_raw(send)

    def send_whisper(self, user: str, message: str):
        send = f"PRIVMSG #{self.nick} :/w {user} {message}"
        self._send_raw(send)
        self.log.whisper(message, user.lower())

    def timeout_user(self, user: str, channel: str, timeout=1):
        send = f"PRIVMSG #{channel} :/timeout {user} {timeout}"
        self._send_raw(send)

    def clear_message(self, channel: str, message_id: str):
        send = f"PRIVMSG #{channel} :/delete {message_id}"
        self._send_raw(send)

    def ban_user(self, user: str, channel: str):
        send = f"PRIVMSG #{channel} :/ban {user}"
        self._send_raw(send)

    def on_socket_data(self, line: str):
        pass