import socket
from threading import * 
from subprocess import PIPE , STDOUT ,Popen

HOST=""
PORT=7071

def Start_new_math_thread(conn,addr):
    t=MathServerCommunicationThread(conn,addr)
    t.start()

# run a stdout in seperate thread 
class ProcessOutputThread(Thread):
    def __init__(self,process,conn):
        Thread.__init__(self)
        self.process=process
        self.conn=conn
    
    def run(self):
        #we handle the exit and quit  input     
        # this thread will not closed so we check connection is closed ot not 
        while not self.process.stdout.closed and not self.conn._closed:
            try:
                self.conn.sendall(self.process.stdout.readline())
            except:
                pass


class MathServerCommunicationThread(Thread):
    def __init__(self,conn,addr):
        Thread.__init__(self)
        self.addr=addr
        self.conn=conn
    def run(self):
        #Connection and port forwarding 
        print("{} Connecting with Back Port => {}".format(addr[0],addr[1]))
        self.conn.sendall("You are Connected into Math Server . Please give some Math Expressions .....\n\n$".encode())
        # get a bc command 
        p=Popen(['bc'],stderr=STDOUT,stdin=PIPE,stdout=PIPE,shell=True)
        # call classes ini thread in proper way 
        out=ProcessOutputThread(p,self.conn)
        out.start()

        while not p.stdout.closed and not self.conn._closed:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                else:
                    try:
                        data=data.decode()
                        query=data.strip()
                        if(query =="exit" or query == "quit"):
                            # here process will be quit  
                            #  we create a multiple instance of single process for each connection 
                            p.communicate(query.encode(),timeout=1)
                            if p.poll() is not None:
                                break
                        query = query + "\n"
                        p.stdin.write(query.encode())
                        p.stdin.flush()
                    except:
                        pass
            except:
                pass
        # if connection is not close it will not exited  same like  line 22
        self.conn.close()


#initilize socket 

s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind((HOST,PORT))
s.listen()
while True:
    conn,addr=s.accept()
    Start_new_math_thread(conn,addr)

s.close()




