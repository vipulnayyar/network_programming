from thread import *
import random
from Tkinter import *
import socket
import sys

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

def mousePressed(event):
    canvas = event.widget.canvas
    redrawAll(canvas)

def keyPressed(event):
    canvas = event.widget.canvas
    global s
    # first process keys that work even if the game is over
    if (event.char == "q"):
        gameOver(canvas)
    elif (event.char == "r"):
        init(canvas)
    elif (event.char == "d"):
        canvas.data["inDebugMode"] = not canvas.data["inDebugMode"]
    # now process keys that only work if the game is not over
    if (canvas.data["isGameOver"] == False):
        if (event.keysym == "Up"):
            s.sendall("UP")
            moveSnake(canvas, -1, 0,-1)
        elif (event.keysym == "Down"):
            s.sendall("DOWN")
            moveSnake(canvas, +1, 0,-1)
        elif (event.keysym == "Left"):
            s.sendall("LEFT")
            moveSnake(canvas, 0,-1,-1)
        elif (event.keysym == "Right"):
            s.sendall("RIGHT")
            moveSnake(canvas, 0,+1,-1)
    redrawAll(canvas)

def moveSnake(canvas, drow, dcol,pl):
    snakeBoard = canvas.data["snakeBoard"]
    print "vdf"
    rows = len(snakeBoard)
    cols = len(snakeBoard[0])
    if pl==1:
    	headRow = canvas.data["headRow"]
    	headCol = canvas.data["headCol"]
    elif pl==-1:
    	headRow = canvas.data["remoteRow"]
    	headCol = canvas.data["remoteCol"]
    
    newHeadRow = headRow + drow
    newHeadCol = headCol + dcol
    if ((newHeadRow < 0) or (newHeadRow >= rows) or
        (newHeadCol < 0) or (newHeadCol >= cols)):
        # snake ran off the board
        gameOver(canvas)
    elif (snakeBoard[newHeadRow][newHeadCol] != 0 and snakeBoard[newHeadRow][newHeadCol] < 100):
        # snake ran into itself!
        gameOver(canvas)
    else:
        snakeBoard[newHeadRow][newHeadCol] = pl *(1 + abs(snakeBoard[headRow][headCol]));
        if pl==1:
        	canvas.data["headRow"] = newHeadRow
        	canvas.data["headCol"] = newHeadCol
        elif pl==-1:
        	canvas.data["remoteRow"] = newHeadRow
        	canvas.data["remoteCol"] = newHeadCol
        
        removeTail(canvas,pl)

def removeTail(canvas,pl):
    # find every snake cell and subtract 1 from it.  When we're done,
    # the old tail (which was 1) will become 0, so will not be part of the snake.
    # So the snake shrinks by 1 value, the tail.
    snakeBoard = canvas.data["snakeBoard"]
    rows = len(snakeBoard)
    cols = len(snakeBoard[0])
    for row in range(rows):
        for col in range(cols):
            if (snakeBoard[row][col] > 0 and snakeBoard[row][col] < 100 and pl ==1):
                snakeBoard[row][col] = snakeBoard[row][col] - 1
			
            if (snakeBoard[row][col] < 0 and pl == -1):
				snakeBoard[row][col] = snakeBoard[row][col] + 1

def gameOver(canvas):
    canvas.data["isGameOver"] = True

def timerFired(canvas):
    if (canvas.data["isGameOver"] == False):
        # only process timerFired if game is not over
        redrawAll(canvas)
    # whether or not game is over, call next timerFired
    # (or we'll never call timerFired again!)
    delay = 250 # milliseconds
    canvas.after(delay, timerFired, canvas) # pause, then call timerFired again

def redrawAll(canvas):
    canvas.delete(ALL)
    drawSnakeBoard(canvas)
    if (canvas.data["isGameOver"] == True):
        canvas.create_text(155, 155, text="Game Over!", font=("Helvetica", 32, "bold"))

def drawSnakeBoard(canvas):
    snakeBoard = canvas.data["snakeBoard"]
    rows = len(snakeBoard)
    cols = len(snakeBoard[0])
    for row in range(rows):
        for col in range(cols):
            drawSnakeCell(canvas, snakeBoard, row, col)

def drawSnakeCell(canvas, snakeBoard, row, col):
    margin = 5
    cellSize = 30
    left = margin + col * cellSize
    right = left + cellSize
    top = margin + row * cellSize
    bottom = top + cellSize

    canvas.create_rectangle(left, top, right, bottom, fill="white")
    if (snakeBoard[row][col] > 0 and snakeBoard[row][col] < 100):
        # draw part of the snake body
        canvas.create_oval(left, top, right, bottom, fill="blue")
    elif (snakeBoard[row][col] < 0 ):
        # draw part of the snake body
        canvas.create_oval(left, top, right, bottom, fill="red")
    elif (snakeBoard[row][col] == 100):
        # draw food
        canvas.create_oval(left, top, right, bottom, fill="green")
    # for debugging, draw the number in the cell
    if (canvas.data["inDebugMode"] == True):
        canvas.create_text(left+cellSize/2,top+cellSize/2,
                           text=str(snakeBoard[row][col]),font=("Helvatica", 14, "bold"))

def loadSnakeBoard(canvas):
    snakeBoard = [ [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
                   [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
                   [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
                   [ 0, 0, 0, 0, 4, 5, 0, 0, 0, 0 ],
                   [ 0, 0, 0, 0, 3, 0, 0, 0, 0, 0 ],
                   [ 0, 0, 0, 1, 2, 0, 0, 0, 0, 0 ],
                   [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
                   [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
                   [ 0, 0, 0, 0, 0, 0, -5, 0, 0, 0 ],
                   [ 0, 0, 0, 0, 0, 0, -4, -3, -2, -1 ]
                ]
    canvas.data["snakeBoard"] = snakeBoard
    findSnakeHead(canvas)
    #placeFood(canvas)

def placeFood(canvas):
    # place food (-1) in a random location on the snakeBoard, but
    # keep picking random locations until we find one that is not
    # part of the snake!
    snakeBoard = canvas.data["snakeBoard"]
    rows = len(snakeBoard)
    cols = len(snakeBoard[0])
    while True:
        row = random.randint(0,rows-1)
        col = random.randint(0,cols-1)
        if (snakeBoard[row][col] == 0):
            break
    snakeBoard[row][col] = 100

def findSnakeHead(canvas):
    # find where snakeBoard[row][col] is largest, and
    # store this location in headRow, headCol
    snakeBoard = canvas.data["snakeBoard"]
    rows = len(snakeBoard)
    cols = len(snakeBoard[0])
    headRow = 0
    headCol = 0
    for row in range(rows):
        for col in range(cols):
            if (snakeBoard[row][col] > snakeBoard[headRow][headCol] and snakeBoard[row][col] < 100):
                headRow = row
                headCol = col
    canvas.data["headRow"] = headRow
    canvas.data["headCol"] = headCol
    canvas.data["remoteRow"] = 8
    canvas.data["remoteCol"] = 6

def printInstructions():
    print "Snake!"
    print "Use the arrow keys to move the snake."
    print "Eat food to grow."
    print "Stay on the board!"
    print "And don't crash into yourself!"
    print "Press 'd' for debug mode."
    print "Press 'r' to restart."

def init(canvas):
    printInstructions()
    loadSnakeBoard(canvas)
    canvas.data["inDebugMode"] = False
    canvas.data["isGameOver"] = False
    redrawAll(canvas)

########### copy-paste below here ###########


root = Tk()
canvas = Canvas(root, width=310, height=310)
canvas.pack()
# Store canvas in root and in canvas itself for callbacks
root.canvas = canvas.canvas = canvas
# Set up canvas data and call init
canvas.data = { }
init(canvas)
# set up events
root.bind("<Button-1>", mousePressed)
root.bind("<Key>", keyPressed)
#timerFired(canvas)


def thread(canvas):
	print "thread "
	global s
	while 1:
		data = str.split(s.recv(1024))[0]
		print "msg " + data
		if data == "UP":
			print "up"
			moveSnake(canvas, -1, 0,+1)
		elif data=="DOWN":
			print "down"
			moveSnake(canvas, +1, 0,+1)
		elif data=="LEFT":
			print "left"
			moveSnake(canvas, 0, -1,+1)
		elif data=="RIGHT":
			print "right"
			moveSnake(canvas, 0, +1,+1)
		print canvas.data["snakeBoard"]
		redrawAll(canvas)



start_new_thread(thread,(canvas,))

# and launch the app
root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)
