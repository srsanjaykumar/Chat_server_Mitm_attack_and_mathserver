import socket as s
from threading import Thread

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

class ChatServerThread(Thread):
    def __init__(self,conn ,addr):
        Thread.__init__(self)
        self.conn=conn
        self.addr=addr
        self.username=""
        self.user_ip=addr[0]
        self.user_port=addr[1]
    
    def setUserName(self,name):
        self.username=name
    
    def isClosed(self):
        return self.conn._closed
    
    def run(self):
        pass


#  it can accept any interface connection 
#  to see the network interface  using command ifconfig=>linux  ipconfig => windows

HOST = ''
PORT = 9988
binding = (HOST, PORT)
sock = s.socket(s.AF_INET, s.SOCK_STREAM)
# AF_INET is a Domain name or IPv4 and SOCK_STREAM is a TCP communication
sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, True)
# To avoid Address already in use 
sock.bind( binding )
# Combine the host and port 
sock.listen()
# Accept n number of Connections 

print(sock._closed)

# here we accept multiple connections 
while not sock._closed:
    conn ,addr = sock.accept()



# final once we chack if socket is not closed we close the socket 
if not sock._closed:
    sock.close()

# print(sock._closed)  # returns true