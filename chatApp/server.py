#Name: Shet Neha Nilcant and UTA ID: 1001387308

import socket 
import sys
from time import *;
from threading import Thread
import simplejson

peerlist = {};

class ServerThread(Thread):
    
     def __init__(self,ip,port,socket):

            #initialise the variables to be used by the thread
            Thread.__init__(self)
            self.ip = ip
            self.port = port
            self.socket = socket
            self.username = '';
            self.peername = '';
            self.client = 1;
            print "A New thread has been created for Client Socket with IP:"+ip+" Port Number:"+str(port)
    
     def run(self):
        
        while True:
            try:
                self.socket.settimeout(60);
                flag = 0;
                data = self.socket.recv(1024)
                recvData = simplejson.loads(data);
                #print recvData;
                header = recvData["header"];
                msg = recvData["msg"];
                data = msg.strip().lower().split(":");
                
                
                if(data[0] == "user"):
		    #check if the username already exists
		    for thread in threads:
			if(thread.username == data[1].strip().lower()):
				self.socket.send("error:Please enter a different name. User with this name already exists");
				break;

                    self.username = data[1].strip().lower();
                    #print self.username;
                    #self.socket.send('HTTP/1.1 200 OK\n') #send the header to the client with 200 OK status
                    for peer in peerlist:
                        if(self.username == peer):
                            flag = 1;
                            self.peername = peerlist[peer];
                            self.client = 2;
                            self.socket.send("peerSuccess:"+self.peername+":"+str(self.client));
                            break;

                    if(flag == 0):
                        self.socket.send("success:"+str(self.client));
		    
                elif(data[0].strip().lower() == "peer"):
                    self.peername = data[1].strip().lower();
                    peerlist[self.peername] = self.username;
                    #self.socket.send('HTTP/1.1 200 OK\n') #send the header to the client with 200 OK status
                    self.socket.send("success");
                elif(data[0].strip().lower() == "chat"):
                    # close the socket and inform the client 
                    if(data[1].strip().lower() == "quit"):
                        
                        user_disconnect = self.username;
                        for thread in threads:
                            if thread.peername == user_disconnect:
                                thread.peername = '';
                                key = thread.username;
                                
                                if key in peerlist.keys():
                                    del peerlist[key];
                                else:
                                    del peerlist[user_disconnect];
                                http = "HTTP/1.1 200 OK "+ctime();
                                
                                msg = '{"header":"'+http+'","msg":"disconnect:'+user_disconnect+'has disconnected. You can no longer chat"}';
                                thread.socket.send(msg);
                                break;
                        http = "HTTP/1.1 200 OK "+ctime();
                        msg = '{"header":"'+http+'","msg":"disconnect:You have diconnected"}';
                        self.socket.send(msg);
                    connected_peer = self.peername;    
                    print "http Header ",header
                    print "Sender:"+self.username+" Message: "+data[1];
                    
                    
                    
                    for thread in threads:
                        if thread.username == connected_peer:
                            http = "HTTP/1.1 200 OK "+ctime();
                            msg = '{"header":"'+http+'","msg":"'+data[1]+'"}';
                            thread.socket.send(msg);
                            break;

                # check for timeout and also chcek for symbols to check if the client is alive and send message to other user

                    #self.peername = self.socket.recv(1024);

                    #Send the content of the requested file to the client

                    #self.socket.send(outputdata[i])      #send data to the client
            except Exception, e:
                if(self.socket and self.username):
                    user_disconnect = self.username;
                    #print "username",user_disconnect
                    for thread in threads:
                        if thread.peername == user_disconnect:
                            thread.peername = '';
                            key = thread.username;

                            if peerlist.has_key(key):
                                del peerlist[key];
                            else:
                                del peerlist[user_disconnect];
			    
                            http = "HTTP/1.1 200 OK "+ctime();
                            msg = '{"header":"'+http+'","msg":"disconnect:'+user_disconnect+ 'has disconnected. You can no longer chat"}';
                            thread.socket.send(msg);
                            break;
                
                http = "HTTP/1.1 200 OK "+ctime();
                msg = '{"header":"'+http+'","msg":"disconnect:You have diconnected"}';
                #print e
                self.socket.send(msg);

        #self.socket.send('\n Server Socket family : '+str(serverSocket.family)+'\n Serever socket protocol'+ str(serverSocket.proto)+'\n SocketType'+str(serverSocket.type))
        print "\n data sent to the client";
        #self.socket.close()
        print "\n socket is closed";

serverSocket =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #create the socket object to use IP v4 and TCP.       
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #socket.SO_REUSEADDR, causes the port to be released immediately after the socket is closed.


#port would be 8080 if not specified in the command line argument else it would take the value from sys.argv[1]
  
serverSocket.bind(("127.0.0.1",9001)) 
serverSocket.listen(5)
threads = [];
while True:
            
            print "Waiting for incoming connections..."
            conn, address = serverSocket.accept(); #accept the incoming connection through the socket
            
            newThread = ServerThread(address[0],address[1],conn) #create a new thread for the client connect
            print conn;
            newThread.start() #start the thread
            threads.append(newThread) #append the newly created thread to the existing threads array

for thread in threads:
    thread.join()
        
