import Tkinter
from Tkinter import Tk, Button
import socket
import sys  
from thread import *

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

def check(no):
	if arr[no]["text"]=="  X  ":
		return -1
	if arr[no]["text"]=="  O  ":
		return -2
	return no


def buttoncallback(no):
	global key,turn,s,count
	if turn != "yes":
		return
	if arr[no]["text"] == "  X  " or arr[no]["text"] == "  O  ":
		return
	
	arr[no].config(text = "  " + key + "  ")
	count=count+1
	msg="PLAY-"
	
	if check(1) == check(2) == check(3):
		msg="WIN-"
	elif check(4) == check(5) == check(6):
		msg="WIN-"
	elif check(7) == check(8) == check(9):
		msg="WIN-"
	elif check(1) == check(4) == check(7):
		msg="WIN-"
	elif check(2) == check(5) == check(8):
		msg="WIN-"
	elif check(3) == check(6) == check(9):
		msg="WIN-"
	elif check(1) == check(5) == check(9):
		msg="WIN-"
	elif check(3) == check(5) == check(7):
		msg="WIN-"
	elif count == 9:
		msg="TIE-"

	if key == "X":
   		key = "O"
   	else:
   		s.sendall(msg+str(no))
   		turn = "no"
   		key = "X"
   	


arr.append(-1)
A = Tkinter.Button(top, text ="     ", height=3, width=4, command =lambda: buttoncallback(1))
A.grid(row=0,column=0)
arr.append(A)

B = Tkinter.Button(top, text ="     ", height=3, width=4, command =lambda: buttoncallback(2))
B.grid(row=0,column=1)
arr.append(B)

C = Tkinter.Button(top, text ="     ", height=3, width=4, command =lambda: buttoncallback(3))
C.grid(row=0,column=2)
arr.append(C)

D = Tkinter.Button(top, text ="     ", height=3, width=4, command =lambda: buttoncallback(4))
D.grid(row=1,column=0)
arr.append(D)

E = Tkinter.Button(top, text ="     ", height=3, width=4, command =lambda: buttoncallback(5))
E.grid(row=1,column=1)
arr.append(E)

F = Tkinter.Button(top, text ="     ", height=3, width=4, command =lambda: buttoncallback(6))
F.grid(row=1,column=2)
arr.append(F)

G = Tkinter.Button(top, text ="     ", height=3, width=4, command =lambda: buttoncallback(7))
G.grid(row=2,column=0)
arr.append(G)

H = Tkinter.Button(top, text ="     ", height=3, width=4, command =lambda: buttoncallback(8))
H.grid(row=2,column=1)
arr.append(H)

I = Tkinter.Button(top, text ="     ", height=3, width=4, command =lambda: buttoncallback(9))
I.grid(row=2,column=2)
arr.append(I)



def thread(conn):
	print "thread "
	global turn
	while 1:
		if turn == "no":
			data = str.split(conn.recv(1024),'-')
			print data
			if data[0]=="WIN":
				output="WIN"
				break
			if data[0]=="PLAY":
				turn="yes"
				buttoncallback(int(data[1]))
			if data[0]=="TIE":
				output="TIE"
				break

start_new_thread(thread,(s,))

top.mainloop()