import time, random, threading
from tkinter import *
from Stack import *

#10, 9x9
#40, 15x13
#99, 30x16

root = Tk()
difficulties = ['Easy', 'Medium', 'Expert']
difficulty = StringVar(root)
difficulty.set(difficulties[0])
BOUNDS = {'Easy':[8, 8], 'Medium':[14, 12], 'Expert':[29, 15]}

def Start_Game():
    if app.ButtonList != []:
        for row in app.ButtonList:
            for button in row:
                button.destroy()
    if difficulty.get() == 'Easy':
        app.init_beginner_window()
        Main.__init__('Easy')
    elif difficulty.get() == 'Medium':
        app.init_medium_window()
        Main.__init__('Medium')
    else:
        app.init_expert_window()
        Main.__init__('Expert')

class Game:
    def __init__(self, difficulty):
        self.__Time = 0
        self.__Board = []
        self.__Running = True
        self.__Difficulty = difficulty
        self.init_board(self.__Difficulty)
        
    def init_board(self, difficulty):
        self.__MineList = []
        if difficulty == 'Easy':
            while len(self.__MineList) != 10:
                if (New_Mine := [random.randint(0, 8), random.randint(0, 8)]) not in self.__MineList:
                    self.__MineList.append(New_Mine)
            for x in range(9):
                Row = []
                for y in range(9):
                    if [x, y] in self.__MineList:
                        Row.append(Cell('M'))
                    else:
                        Row.append(Cell(0))
                self.__Board.append(Row)
        elif difficulty == 'Medium':
            while len(self.__MineList) != 40:
                if (New_Mine := [random.randint(0, 14), random.randint(0, 12)]) not in self.__MineList:
                    self.__MineList.append(New_Mine)
            for x in range(15):
                Row = []
                for y in range(13):
                    if [x, y] in self.__MineList:
                        Row.append(Cell('M'))
                    else:
                        Row.append(Cell(0))
                self.__Board.append(Row)
        else:
            while len(self.__MineList) != 99:
                if (New_Mine := [random.randint(0, 29), random.randint(0, 15)]) not in self.__MineList:
                    self.__MineList.append(New_Mine)
            for x in range(30):
                Row = []
                for y in range(16):
                    if [x, y] in self.__MineList:
                        Row.append(Cell('M'))
                    else:
                        Row.append(Cell(0))
                self.__Board.append(Row)

        for position in self.__MineList:
            for u in [-1, 0, 1]:
                for v in [-1, 0, 1]:
                    if 0<=position[0]+u<=BOUNDS[difficulty][0] and 0<=position[1]+v<=BOUNDS[difficulty][1]:
                        if (newCell := self.__Board[position[0]+u][position[1]+v]).GetValue() != 'M':
                            newCell.IncrementValue()
        
    def LeftClick(self, index):
        if self.__Running == False:
            return None
        cell = self.__Board[index[0]][index[1]]
        if cell.GetSolved():
            return None
        if cell.GetFlagged():
            return None
        else:
            if cell.GetValue() == 'M':
                self.EndGame('loss')
            else:
                if cell.GetValue() == 0:
                    s = ' '
                else:
                    s = str(cell.GetValue())
                app.ButtonList[index[0]][index[1]].config(text=s, relief='sunken')
                cell.SetSolved()
                if cell.GetValue() == 0:
                    self.__ClearArea(index)
                self.CheckWin()

    def RightClick(self, index):
        if self.__Running == False:
            return None
        cell = self.__Board[index[0]][index[1]]
        if cell.GetSolved():
            return None
        if cell.GetFlagged() == True:
            app.ButtonList[index[0]][index[1]].config(text='')
        else:
            app.ButtonList[index[0]][index[1]].config(text='🏴')
        cell.Flag()
    
    def __ClearArea(self, pos):
        stack = Stack()
        stack.push(pos)
        while stack.length() != 0:
            index = stack.pop()
            node = self.__Board[index[0]][index[1]]
            if node.GetSolved() == False or index == pos:
                node.SetSolved()
                app.ButtonList[index[0]][index[1]].config(text='', relief='sunken')
                for u in [-1, 0, 1]:
                    for v in [-1, 0, 1]:
                        if 0<=index[0]+u<=BOUNDS[self.__Difficulty][0] and 0<=index[1]+v<=BOUNDS[self.__Difficulty][1]:
                            newIndex = [index[0]+u, index[1]+v]
                            neighbour = self.__Board[newIndex[0]][newIndex[1]]
                            if neighbour.GetSolved() == False:
                                if neighbour.GetValue() == 0:
                                    stack.push(newIndex)
                                else:
                                    neighbour.SetSolved()
                                    app.ButtonList[newIndex[0]][newIndex[1]].config(text=str(neighbour.GetValue()), relief='sunken')

    def EndGame(self, state):
        self.__Running = False
        if state == 'win':
            print('you won')
        else:
            print('you lose :(')
            for index in self.__MineList:
                app.ButtonList[index[0]][index[1]].config(text='💣')
    
    def CheckWin(self):
        for Row in self.__Board:
            for cell in Row:
                if cell.GetSolved() == False and cell.GetValue() != 'M':
                    return False
        self.EndGame('win')

    def Start_Timer(self):
        while True:
            if self.__Running == True:
                self.__Time += 0.1
                time.sleep(0.1)
                app.Timer_Label.config(text=str(int(self.__Time)))
    
    def ShowBoard(self):
        for r in range(len(self.__Board)):
            for t in range(len(self.__Board[r])):
                #print(f"R: {r}, T: {t}, Len: {len(app.ButtonList)}")
                b = app.ButtonList[r][t]
                b.config(text=str(self.__Board[r][t].GetValue()))

class Cell:
    def __init__(self, Value):
        self.__Value = Value
        self.__Flagged = False
        self.__Solved = False
    
    def GetValue(self):
        return self.__Value
    
    def IncrementValue(self):
        self.__Value += 1
    
    def GetFlagged(self):
        return self.__Flagged
    
    def Flag(self):
        if self.__Flagged == True:
            self.__Flagged = False
        else:
            self.__Flagged = True

    def GetSolved(self):
        return self.__Solved
    
    def SetSolved(self):
        self.__Solved = True

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self)
        self.master=master
        root.title("Minesweeper")
        self.Timer_Label = Label(text=0)
        self.__diffDropBox = OptionMenu(root, difficulty, *difficulties)
        self.__StartButton = Button(text='New Game', command=lambda:Start_Game())
        self.init_beginner_window()
        #Button(text='S', command=Main.ShowBoard).place(x=0, y=0)
        
    def init_beginner_window(self):
        root.geometry("225x300")
        self.ButtonList = []
        for r in range(0, 9):
            tempRow = []
            for t in range(0, 9):
                newIndex = [r, t]
                newButton = Button(width=2, height=1, command=lambda index=newIndex:Main.LeftClick(index))
                newButton.bind('<Button-3>', lambda event, index=newIndex:Main.RightClick(index))
                tempRow.append(newButton)
                newButton.place(x=r*25, y=t*25+25)
            self.ButtonList.append(tempRow)
        self.__diffDropBox.place(x=15, y=260)
        self.__StartButton.place(x=112, y=262)
        self.Timer_Label.place(x=106)

    def init_medium_window(self):
        root.geometry("374x385")
        self.ButtonList = []
        for r in range(0, 15):
            tempRow = []
            for t in range(0, 13):
                newIndex = [r, t]
                newButton = Button(width=2, height=1, command=lambda index=newIndex:Main.LeftClick(index))
                newButton.bind('<Button-3>', lambda event, index=newIndex:Main.RightClick(index))
                tempRow.append(newButton)
                newButton.place(x=r*25, y=t*25+25)
            self.ButtonList.append(tempRow)
        self.__diffDropBox.place(x=80, y=352)
        self.__StartButton.place(x=200, y=354)
        self.Timer_Label.place(x=175)
    
    def init_expert_window(self):
        root.geometry("750x460")
        self.ButtonList = []
        for r in range(0, 30):
            tempRow = []
            for t in range(0, 16):
                newIndex = [r, t]
                newButton = Button(width=2, height=1, command=lambda index=newIndex:Main.LeftClick(index))
                newButton.bind('<Button-3>', lambda event, index=newIndex:Main.RightClick(index))
                tempRow.append(newButton)
                newButton.place(x=r*25, y=t*25+25)
            self.ButtonList.append(tempRow)
        self.__diffDropBox.place(x=320, y=428)
        self.__StartButton.place(x=410, y=430)
        self.Timer_Label.place(x=390)

Main = Game('Easy')
threading.Thread(target=Main.Start_Timer, args=()).start()
app = Window(root)
root.mainloop()
