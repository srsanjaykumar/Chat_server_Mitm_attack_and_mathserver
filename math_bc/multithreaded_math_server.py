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

# get a bc command 
p=Popen(['bc'],stderr=STDOUT,stdin=PIPE,stdout=PIPE)
t=Thread(target=ProcessOutputThread,args=(p,))
t.start()

