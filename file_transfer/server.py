import socket
import sys
from thread import *
 
HOST = ''   
PORT = 8888 
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 

s.listen(10)
print 'Socket now listening'
 

def clientthread(conn):
    fi = open("received.txt","w+")
    while True:
        data = conn.recv(1024)
        print "receiving"
        print data
        if data  == "^]" :
            break  
        if not data:
            break  
        fi.write(data)

    
    conn.close()
 
while 1:
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
     
    start_new_thread(clientthread ,(conn,))
 
s.close()