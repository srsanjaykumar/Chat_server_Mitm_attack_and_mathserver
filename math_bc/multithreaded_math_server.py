import socket
from threading import * 
from subprocess import PIPE , STDOUT ,Popen

HOST=""
PORT=7070
# run a stdout in seperate thread 
class ProcessOutputThread(Thread):
    def __init__(self,process,conn):
        Thread.__init__(self)
        self.process=process
        self.conn=conn
    
    def run(self):
        while not self.process.stdout:
            self.conn.sendall(self.process.stdout.readline())



#initilize socket 

s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind((HOST,PORT))
s.listen()
addr,conn=s.accept()
#Connection and port forwarding 
print("{} Connecting with Back Port => {} ".format(addr[0],addr[1]))
print("You are Connected into Math Server . Please give some Math Expressions .....\n\n :> $\t")
# get a bc command 
p=Popen(['bc'],stderr=STDOUT,stdin=PIPE,stdout=PIPE,shell=True)
t=Thread(target=ProcessOutputThread,args=(p,conn))
t.start()






