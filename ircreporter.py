import socket
import random
import thread
import re
import threading
class IRCReporter:

    PRE_NICK = "bluebox"
    USER_HOST = "bluebox"
    USER_SERVER = "bluebox"
    USER_REALNAME = "bluebox parser"
    RECEIVER_NICK = "#aausat4packets"
    IRC_SERVER = "irc.freenode.org"
    IRC_PORT = 6667
    IRC_CHANNEL = "#aausat4packets"
    
    def __init__(self):
        # Generate nick
        self.nick = "{}{}".format(IRCReporter.PRE_NICK, random.randint(0,10000))
        self.cv = threading.Condition()
        self.status = -1
        self.connect()
        thread.start_new_thread(self.__reader__, ())

    def connect(self):
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.irc.connect( (IRCReporter.IRC_SERVER, IRCReporter.IRC_PORT) )
        self.irc.recv(8192)
        # Register
        self.irc.send('NICK {}\r\n'.format(self.nick))
        self.irc.send('USER {}, {}, {} :{}\r\n'.format(
            self.nick, IRCReporter.USER_HOST,
            IRCReporter.USER_SERVER, IRCReporter.USER_REALNAME))
        self.irc.recv(8192)
        # Connect to channel
        self.irc.send('JOIN {}\r\n'.format(IRCReporter.IRC_CHANNEL))
        self.irc.recv(8192)
        self.irc.send('PRIVMSG {} : I have joined!\r\n'.format(IRCReporter.RECEIVER_NICK))

    def send(self, msg):
        lines = msg.replace("\r","").split("\n")
        for line in lines:
            self.irc.send('PRIVMSG {} :{}\r\n'.format(IRCReporter.RECEIVER_NICK, line))

    def verify_packet(self, hex_packet):
        #self.cv.acquire()
        self.irc.send("AUTH,1,{}".format(hex_packet[0:len(hex_packet)/2]))
        self.irc.send("AUTH,2,{}".format(hex_packet[len(hex_packet)/2:]))
        #self.cv.wait()
        #self.cv.release()
        #ret_val = self.status
        #self.status -1
        #return ret_val

    def __reader__(self):
        #self.cv.acquire()
        for line in self.irc.makefile():
            m = re.search(r'{}:(GOOD)\r\n'.format(self.nick), line)
            if m:
                print m
        #self.cv.notify()
        #self.cv.release()    
