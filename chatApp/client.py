from socket import *
from select import *
import sys;
from time import *;
import simplejson

# Information of our server to connect to
HOST = "127.0.0.1"
PORT = 9001 #port 80
client = 1;

sock = socket(AF_INET, SOCK_STREAM)

def takeInput():
    #Takes the user name	
    username = raw_input(); 
    #build the header
    http = "HTTP/1.1 200 OK "+ctime();
    #generates a string with username and header
    msg = '{"header":"'+http+'","msg":"user:'+username+'"}';
    #send message to the server
    sock.send(msg);
    #Receive data from the server
    recvData = sock.recv(1024);
    	
    data = recvData.split(":");
    #It checks server message if the username with same name already exists
    if(data[0] == "error"):
  	print "Please Enter different name:"
	takeInput();
	
    elif(data[0] == "success"):
    	client = int(data[1]);
        print "Enter peer name:"
        peername = raw_input();
        if(len(peername)):
            
        	http = "HTTP/1.1 200 OK "+ctime();
            	msg = '{"header":"'+http+'","msg":"peer:'+peername+'"}';
            	sock.send(str.encode(msg));
            	peerOutput = sock.recv(1024)
            	print peerOutput;
    else:
        client = int(data[2]);
        print "you are connected to "+data[1];

try:
    sock.connect((HOST, PORT))
    sock.settimeout(60);
    # Client loop
    # Let the user enter some data to send
    print "Enter your username:";
    takeInput();
    #print data
    
 
    sys.stdout.write('Me: '); sys.stdout.flush()

    while 1:
        socket_list = [sys.stdin, sock]

        # Get the list sockets which are readable
        ready_to_read,ready_to_write,in_error = select(socket_list , [], [])

        for s in ready_to_read:             
            if s == sock:
                # incoming message from remote server, s
                data = sock.recv(4096)
                recvData = simplejson.loads(data);
                header = recvData["header"];
                msg = recvData["msg"];
                if not data :
                    print '\nDisconnected from chat server'
                    sys.exit()
                else :

                    chatData = msg.split(":");
                    if(chatData[0] == "disconnect"):
                        sys.stdout.write(chatData[1]);
                        sys.exit();
		    sys.stdout.write('\nOther:');
                    sys.stdout.write(chatData[0])
		    sys.stdout.write('\nMe:');
                    sys.stdout.flush()     

            else :
                # user entered a message
                http = "HTTP/1.1 200 OK "+ctime();
                msg = '{"header":"'+http+'","msg":"chat:'+sys.stdin.readline().strip()+'"}';
                #print msg
                sock.send(msg)
                sys.stdout.write('Me:'); sys.stdout.flush()

except Exception,e:
    print "\nconnection is closed";
    sys.exit();
