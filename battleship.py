"""
Battleship Project
Name:
Roll No:
"""

import battleship_tests as test

project = "Battleship" # don't edit this

### SIMULATION FUNCTIONS ###

from tkinter import *
import random

EMPTY_UNCLICKED = 1
SHIP_UNCLICKED = 2
EMPTY_CLICKED = 3
SHIP_CLICKED = 4


'''
makeModel(data)
Parameters: dict mapping strs to values
Returns: None
'''
def makeModel(data):

    data["rows"] = 10
    data["cols"] = 10
    data["board_Size"] = 500
    data["cell_Size"] = data["board_Size"]/data["rows"]
    data["numShips"] = 5
    data["user_Ship_Num"]=0
    data["comp_Ship_Num"]=5
    data["user_Board"]=emptyGrid(data["rows"],data["cols"])
    data["comp_Board"]=addShips(emptyGrid(data["rows"],data["cols"]),data["numShips"])
    data["temp_Ship"]=[]
    #data["user_Ships"]=0
    data["winner_Track"]=None
    data["max_Num_Turns"]=50
    data["current_Num_Turns"]=0
    
    return data

'''
makeView(data, userCanvas, compCanvas)
Parameters: dict mapping strs to values ; Tkinter canvas ; Tkinter canvas
Returns: None
'''
def makeView(data, userCanvas, compCanvas):
    drawGrid(data, userCanvas, data["user_Board"], True)
    #drawGrid(data, userCanvas, data["user_Board"], False)
    #drawGrid(data, compCanvas, data["comp_Board"], True)
    drawGrid(data, compCanvas, data["comp_Board"], False)
    drawShip(data, userCanvas,data["temp_Ship"])
    drawGameOver(data,userCanvas)
    return


'''
keyPressed(data, events)
Parameters: dict mapping strs to values ; key event object
Returns: None
'''
def keyPressed(data, event):
    if event.keysym=="Return":
        makeModel(data)
    return


'''
mousePressed(data, event, board)
Parameters: dict mapping strs to values ; mouse event object ; 2D list of ints
Returns: None
'''
def mousePressed(data, event, board):
    if data["winner_Track"]!=None:
        return
    click= getClickedCell(data,event)
    if board=="user":
        clickUserBoard(data,click[0],click[1])
    elif board=="comp" and  data["user_Ship_Num"]==5:
        click1= getClickedCell(data,event)
        runGameTurn(data, click1[0], click1[1])
    return

#### WEEK 1 ####

'''
emptyGrid(rows, cols)
Parameters: int ; int
Returns: 2D list of ints
'''
def emptyGrid(rows, cols):
    grid=[]
    for i in range (rows):
        col=[]
        for j in range(cols):
            col.append(EMPTY_UNCLICKED)
        grid.append(col)
    return grid


'''
createShip()
Parameters: no parameters
Returns: 2D list of ints
'''
def createShip():
    rows = random.randint(1,8)
    cols = random.randint(1,8)
    ship_orientation = random.randint(0,1)
    if ship_orientation == 0:
        ship_placing=[[rows-1,cols],[rows,cols],[rows+1,cols]]
    else:
        ship_placing=[[rows,cols-1],[rows,cols],[rows,cols+1]] 
    return ship_placing

'''
checkShip(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def checkShip(grid, ship):
    for each in ship:
        x=each[0]
        y=each[1]
        if grid[x][y] != EMPTY_UNCLICKED:
            return False
    return True

'''
addShips(grid, numShips)
Parameters: 2D list of ints ; int
Returns: 2D list of ints
'''
def addShips(grid, numShips):
    count = 0
    while count < numShips:
        ship = createShip()
        if checkShip(grid,ship) == True:
            for each in ship:
                x=each[0]
                y=each[1]
                grid[x][y] = SHIP_UNCLICKED
            count = count+1
    return grid

'''
drawGrid(data, canvas, grid, showShips)
Parameters: dict mapping strs to values ; Tkinter canvas ; 2D list of ints ; bool
Returns: None
'''
def drawGrid(data, canvas, grid, showShips):
    for row in range(data["rows"]):
        for col in range(data["cols"]):
            if grid[row][col]==SHIP_UNCLICKED and showShips==False:
                canvas.create_rectangle (col*data["cell_Size"],row*data["cell_Size"],col*data["cell_Size"]+data["cell_Size"],row*data["cell_Size"]+data["cell_Size"],fill="blue")
            elif grid[row][col]==SHIP_UNCLICKED:
                canvas.create_rectangle (col*data["cell_Size"],row*data["cell_Size"],col*data["cell_Size"]+data["cell_Size"],row*data["cell_Size"]+data["cell_Size"],fill="yellow")
            elif grid[row][col]==EMPTY_UNCLICKED:
                canvas.create_rectangle (col*data["cell_Size"],row*data["cell_Size"],col*data["cell_Size"]+data["cell_Size"],row*data["cell_Size"]+data["cell_Size"],fill="blue")
            elif grid[row][col]==SHIP_CLICKED:
                canvas.create_rectangle (col*data["cell_Size"],row*data["cell_Size"],col*data["cell_Size"]+data["cell_Size"],row*data["cell_Size"]+data["cell_Size"],fill="red")
            elif grid[row][col]==EMPTY_CLICKED:
                canvas.create_rectangle (col*data["cell_Size"],row*data["cell_Size"],col*data["cell_Size"]+data["cell_Size"],row*data["cell_Size"]+data["cell_Size"],fill="white")
            
    return


### WEEK 2 ###

'''
isVertical(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isVertical(ship):
    ship.sort()
    if ship[0][1]==ship[1][1]==ship[2][1]:
        if ship[0][0]+1==ship[1][0]==ship[2][0]-1:
            return True
    return False

'''
isHorizontal(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isHorizontal(ship):
    ship.sort()
    if ship[0][0]==ship[1][0]==ship[2][0]:
        if ship[0][1]+1==ship[1][1]==ship[2][1]-1:
            return True
    return False

'''
getClickedCell(data, event)
Parameters: dict mapping strs to values ; mouse event object
Returns: list of ints
'''
def getClickedCell(data, event):
    coord_x=int(event.x/data["cell_Size"])
    coord_y=int(event.y/data["cell_Size"])
    return [coord_y,coord_x]
'''
drawShip(data, canvas, ship)
Parameters: dict mapping strs to values ; Tkinter canvas; 2D list of ints
Returns: None
'''
def drawShip(data, canvas, ship):
    for each in ship:
        canvas.create_rectangle(each[1]*data["cell_Size"],each[0]*data["cell_Size"],each[1]*data["cell_Size"]+data["cell_Size"],each[0]*data["cell_Size"]+data["cell_Size"],fill="white") 
    return



'''
shipIsValid(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def shipIsValid(grid, ship):
    if checkShip(grid,ship):
        if isHorizontal(ship) or isVertical(ship):
            return True
    return False

'''
placeShip(data)
Parameters: dict mapping strs to values
Returns: None
'''
def placeShip(data):
    if shipIsValid(data["user_Board"],data["temp_Ship"])==True:
        for each in data["temp_Ship"]:
            data["user_Board"][each[0]][each[1]] = SHIP_UNCLICKED
        data["user_Ship_Num"]+=1
        print("ship can be place")
    else:
        print("Ship is not valid")
    data["temp_Ship"]=[]
    
    return

'''
clickUserBoard(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def clickUserBoard(data, row, col):
    if data["user_Ship_Num"]==5:
        print("Start playing the game")
        return
    if [row,col] in data["temp_Ship"]:
        return
    else:
        data["temp_Ship"].append([row,col])
    if len(data["temp_Ship"])==3:
        placeShip(data)
        

### WEEK 3 ###

'''
updateBoard(data, board, row, col, player)
Parameters: dict mapping strs to values ; 2D list of ints ; int ; int ; str
Returns: None
'''
def updateBoard(data, board, row, col, player):
    if board[row][col]==SHIP_UNCLICKED:
        board[row][col]=SHIP_CLICKED  
    if board[row][col]== EMPTY_UNCLICKED:
        board[row][col]=EMPTY_CLICKED 
    if isGameOver(board)==True:
        data["winner_Track"]=player
    return
    


'''
runGameTurn(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def runGameTurn(data, row, col):
    if data["comp_Board"][row][col]==SHIP_CLICKED or data["comp_Board"][row][col]==EMPTY_CLICKED:
        #print("clicked")
        return
    else:
        updateBoard(data, data["comp_Board"],row,col, "user")
    list1=getComputerGuess(data["user_Board"])     
    updateBoard(data,data["user_Board"],list1[0],list1[1],"comp")
    data["current_Num_Turns"]+=1
    if data["current_Num_Turns"]==data["max_Num_Turns"]:
        data["winner_Track"]="Draw"


'''
getComputerGuess(board)
Parameters: 2D list of ints
Returns: list of ints
'''
def getComputerGuess(board):
    while True:
        row=random.randint(0,9)  
        col=random.randint(0,9)
        if board[row][col]==EMPTY_UNCLICKED or board[row][col]==SHIP_UNCLICKED:
            #print([row,col])
            return [row,col]
    #return [row][col]
'''
isGameOver(board)
Parameters: 2D list of ints
Returns: bool
'''
def isGameOver(board):
    for row in board:
        for col in row:
            if col==SHIP_UNCLICKED:
                print("game done")
                return False        
    return True

'''
drawGameOver(data, canvas)
Parameters: dict mapping strs to values ; Tkinter canvas
Returns: None
'''
def drawGameOver(data, canvas):
    if data["winner_Track"]=="user":
        canvas.create_text(250, 250, text="Congratulations", font="Arial 35 bold")
        canvas.create_text(300, 300, text=" press Enter to play again", font="Arial 15 bold")
    if data["winner_Track"]=="comp":
        canvas.create_text(250, 250, text="User lost the game", font="Arial 35 bold")
        canvas.create_text(300, 300, text=" press Enter to play again", font="Arial 15 bold")
    if data["winner_Track"]=="Draw":
        canvas.create_text(250, 250, text="Game Draw", font="Arial 35 bold")
        canvas.create_text(300, 300, text=" press Enter to play again", font="Arial 15 bold")
    return


### SIMULATION FRAMEWORK ###

from tkinter import *

def updateView(data, userCanvas, compCanvas):
    userCanvas.delete(ALL)
    compCanvas.delete(ALL)
    makeView(data, userCanvas, compCanvas)
    userCanvas.update()
    compCanvas.update()

def keyEventHandler(data, userCanvas, compCanvas, event):
    keyPressed(data, event)
    updateView(data, userCanvas, compCanvas)

def mouseEventHandler(data, userCanvas, compCanvas, event, board):
    mousePressed(data, event, board)
    updateView(data, userCanvas, compCanvas)

def runSimulation(w, h):
    data = { }
    makeModel(data)

    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window

    # We need two canvases - one for the user, one for the computer
    Label(root, text = "USER BOARD - click cells to place ships on your board.").pack()
    userCanvas = Canvas(root, width=w, height=h)
    userCanvas.configure(bd=0, highlightthickness=0)
    userCanvas.pack()

    compWindow = Toplevel(root)
    compWindow.resizable(width=False, height=False) # prevents resizing window
    Label(compWindow, text = "COMPUTER BOARD - click to make guesses. The computer will guess on your board.").pack()
    compCanvas = Canvas(compWindow, width=w, height=h)
    compCanvas.configure(bd=0, highlightthickness=0)
    compCanvas.pack()

    makeView(data, userCanvas, compCanvas)

    root.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    compWindow.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    userCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "user"))
    compCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "comp"))

    updateView(data, userCanvas, compCanvas)

    root.mainloop()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":
    test.testIsGameOver()
    ## Finally, run the simulation to test it manually ##
    runSimulation(500, 500)
