import socket as s
from threading import Thread
from time import sleep
"""
Goals : 
------------
    1.It has to be multithreaded 
    2.It has to be a group chat 
    3.One messages to be delevered to connected clinets
    4.Server has get a username before join the chat 
    5.Tell when a person connects and tell once a person leave 
    6.Message length 1024 
"""


class ChatBotThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        # Maintain active threads
        self.threads = []
        self.messages=[]

    # each connecting thread added into the array 
    def addChatThread(self, thread):
        self.threads.append(thread)
    
    # if we kill the thread we romove the thread otherwise it will through error
    def removeChatThread(self,thread):
        if thread in self.threads:
            self.threads.remove(thread)


    # format message to the user send in to the thread
    def queueMessages(self,user,message):
        data=(user,message)
        self.messages.append(data)
    def run(self):
        while True:
            sleep(0.025) #25 mill second
            if len(self.messages) > 0:
                for thread in self.threads:
                    for data in self.messages:
                        user=data[0]
                        msg = data[1]
                        if thread.getUserName() != user:
                            thread.sendMessage(msg)



class ChatServerOutgoingThread(Thread):
    # we can access all the methods in IncomingThread Class  because we the object of incoming class
    def __init__(self, incoming_thread):
        Thread.__init__(self)
        self.incoming_thread = incoming_thread
        self.messages = []
        self.can_kill = False

    def sendMessage(self, message):
        fMessage = "{username} : {message} ".format(
            username=self.incoming_thread.getUserName(), message=message)
        try:
            self.incoming_thread.getConnection().sendall(fMessage.encode())
        except:
            bot.removeChatThread(self.incoming_thread)
            # connection is closed  we kill the thread
            self.kill_Thread()

    def kill_Thread(self, should_inform=False):
        # inform others  that the user has disconnected
        self.can_kill = True

    def queueMessage(self, message):
        self.messages.append(message)

    def run(self):
        while True:
            sleep(0.1)  # 100 milliseconds
            if self.can_kill:
                break  # if loop breaks thread has been ended
            if (len(self.messages) > 0):
                for message in self.messages:
                    try:
                        self.sendMessage(message)
                    except:
                        # inform Ohers clients has disconnected
                        break


class ChatServerIncomingThread(Thread):
    def __init__(self, conn, addr):
        # initilize thread from here
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.username = ""
        self.user_ip = addr[0]
        self.user_port = addr[1]
        self.incoming_thread = None
        self.can_kill = False

    def setUserName(self, name):
        self.username = name

    def isClosed(self):
        return self.conn._closed

    def getUserName(self):
        return self.username

    def getConnection(self):
        return self.conn
    
    # see how it work  
    def sendMessage(self,message):
        self.incoming_thread.queueMessage(message)


    def initSendMessageThread(self):
        self.incoming_thread = ChatServerOutgoingThread(self)

    def killThread(self):
        self.can_kill = True

    #  Run is the main part of thread if run is end the thread will closed

    def run(self):
        while not self.conn._closed:
            data = self.conn.recv(2048)
            if not data:  # means the clinent has disconnected
                # inform others when the client has disconnected
                self.incoming_thread.kill_Thread()
                break
            if data.decode().strip() == "kill":
                self.killThread();
            else:
                bot.queueMessages(self.getUserName(), data.decode().strip())


#  it can accept any interface connection
#  to see the network interface  using command ifconfig=>linux  ipconfig => windows

HOST = ''
PORT = 9988

bot = ChatBotThread()

binding = (HOST, PORT)
sock = s.socket(s.AF_INET, s.SOCK_STREAM)
# AF_INET is a Domain name or IPv4 and SOCK_STREAM is a TCP communication
sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, True)
# To avoid Address already in use
sock.bind(binding)
# Combine the host and port
sock.listen()
# Accept n number of Connections

print(sock._closed)

# here we accept multiple connections
while not sock._closed:
    conn, addr = sock.accept()
    t = ChatServerIncomingThread(conn, addr)
    t.start()
    bot.addChatThread(t)
# final once we chack if socket is not closed we close the socket
if not sock._closed:
    sock.close()

# print(sock._closed)  # returns true
