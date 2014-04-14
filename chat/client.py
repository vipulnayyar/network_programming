import Tkinter
import socket
import sys
from Tkinter import *
from thread import *


def encrypt(text,key):
	cur=0
	i=0
	arr=[]
	innerlist=[]

	for i in range(0,len(key)):
		innerlist.append((key[i],i))

	arr.append(innerlist)

	while 1:
		innerlist=[]
		for j in xrange(0,len(key)):
			while cur < len(text):
				if text[cur]==' ' or text[cur]=='\t' or text[cur]=='\n':
					cur=cur+1
				else:
					break	

			if cur < len(text):
				innerlist.append(text[cur])
				cur=cur+1
			else:
				innerlist.append('~')

		arr.append(innerlist)		
		if cur >= len(text):
			break

	for i in xrange(1,len(arr)):
		for j in arr[i]:
	  		sys.stdout.write(j)
	  	print

	s=sorted(arr[0], key=lambda k: k[0])
	#print s

	output=""
	for i in xrange(0,len(s)):
		for j in xrange(1,len(arr)):
			output+=str(arr[j][s[i][1]])	

	return output

def decrypt(text,key):
	arr=[]
	for i in xrange(0,len(text)/len(key)):
		innerlist=[]
		for j in xrange(0,len(key)):
			innerlist.append(0)
		arr.append(innerlist)

	innerlist=[]
	for i in range(0,len(key)):
		innerlist.append((key[i],i))
	s=sorted(innerlist, key=lambda k: k[0])

	cur=0
	for i in xrange(0,len(s)):
		for j in xrange(0,len(arr)):
			arr[j][s[i][1]]=text[cur]
			cur=cur+1

	output=""
	for i in xrange(0,len(arr)):
		for j in xrange(0,len(key)):
			output+=str(arr[i][j])	

	return output


top = Tkinter.Tk()
arr=[]
count=0
key="O"
turn="yes"

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()
     
print 'Socket Created'
 
port = 8889;
 
remote_ip = "127.0.0.1"
 
s.connect((remote_ip , port))
 
print 'Socket Connected on ip ' + remote_ip


text = Text(top)
text.pack()

L1 = Label(top, text="Message")
L1.pack( side = LEFT)
E1 = Entry(top, bd =5)

E1.pack(side = LEFT)



def buttonCallBack():
	global s
	s.sendall(encrypt(E1.get(),"abcd"))   
	text.insert(INSERT, "\n" + "User: " + E1.get())

B = Tkinter.Button(top, text ="Send", command = buttonCallBack)
B.pack(side = RIGHT)


def thread(s):
	print "thread "
	global text
	while 1:
		data = s.recv(1024)
		text.insert(INSERT, "\n" + "Remote: " + str.strip(decrypt(data,"abcd"),'~'))


start_new_thread(thread,(s,))
top.mainloop()