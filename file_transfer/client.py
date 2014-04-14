import Tkinter,tkFileDialog
import sys
import socket
from Tkinter import *

root = Tk()

l1 = Label(root, text="IP Address of server :")
l1.pack( side = LEFT)
e1 = Entry(root, bd =5)
e1.pack(side = LEFT)

l2 = Label(root, text="Port no :")
l2.pack( side = LEFT)
e2 = Entry(root, bd =5)
e2.pack(side = LEFT)

def buttoncallback():
  file = tkFileDialog.askopenfile(parent=root,mode='rb',title='Select a file to send over the network')
  
  s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

  print e1.get()
  host=e1.get()
  port= int(e2.get())

  print host
  print port
  s.connect((host,port))

  if file != None:
    data = file.read()
    # s.sendall("start")
    s.sendall(data)
    s.sendall("^]")
    file.close()
    print "I got %d bytes from this file." % len(data)
    print file


w=Button(root,text ="Click a file to send over the network", command = buttoncallback)
w.pack()
print e1.get()
root.mainloop()