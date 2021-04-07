import tkinter as tk

#Class for single cell object
class Cell():

    def __init__(self, master, x, y, size):
        """ Constructor of the object called by Cell(...) """
        self.master = master
        self.abs = x
        self.ord = y
        self.size= size
        self.fill= False


    def draw(self,tag):
        xmin = self.abs * self.size
        xmax = xmin + self.size
        ymin = self.ord * self.size
        ymax = ymin + self.size

        cell = self.master.canvas.create_rectangle(xmin, ymin, xmax, ymax, fill = "white", outline = "black", activefill="black", tag=tag)
        return cell

class GameBoard(tk.Frame):
    #initialization of tkinter frame, canvas, buttons
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.canvas = tk.Canvas(self, width=500, height=500, background="bisque")
        self.xsb = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.ysb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set)
        self.canvas.configure(scrollregion=(500,500,1000,1000))

        self.xsb.grid(row=1, column=0, sticky="ew")
        self.ysb.grid(row=0, column=1, sticky="ns")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.startButton = tk.Button(self, text="Start", command=self.startGame)
        self.startButton.grid(row=2,column=0)

        self.stopButton = tk.Button(self, text="Stop", command=self.stop)
        self.stopButton.grid(row=2, column=1)

        self.resetButton = tk.Button(self, text="Reset", command=self.reset)
        self.resetButton.grid(row=2, column=2)

        self.genSpeed = tk.Scale(self, from_=0.10, to=2.0, tickinterval=0.1, resolution=0.1)
        self.genSpeed.grid(row=0,column=2)
        self.genSpeed.set(1)

        #default setting of program stop variable
        self.stopped = False

        #coordinate dictionary that stores tags of each cell
        self.coords = {}

        #creates cell objects for grid
        self.grid = []
        for row in range(100):
            line = []
            for column in range(100):
                line.append(Cell(self, column, row, 20))
            self.grid.append(line)
        self.draw()


        #Bind left click to change cell alive/dead:
        self.canvas.bind("<ButtonPress-1>",self.change)

        #linux scroll
        self.canvas.bind("<Button-4>", self.zoomerP)
        self.canvas.bind("<Button-5>", self.zoomerM)
        #windows scroll
        self.canvas.bind("<MouseWheel>",self.zoomer)

        #bind right click and hold to pan window
        self.canvas.bind("<ButtonPress-3>", self.move_start)
        self.canvas.bind("<B3-Motion>", self.move_move)

    #Draws each cell on canvas and adds cell to coordinate array
    def draw(self):
        index = 0
        for row in self.grid:
            for cell in row:
                addCell = cell.draw(str(index))
                index = index +1
                self.coords[str(index)] = addCell


    # def _eventCoords(self, event):
    #     row = int(event.y / self.size)
    #     column = int(event.x / self.size)
    #     return row, column

    #Changes cell alive/dead
    def change(self):
        clickedCell = self.canvas.find_withtag("current")
        fill = self.canvas.itemcget(clickedCell,"fill")
        if(fill == "black"):
            self.canvas.itemconfigure(clickedCell, fill="white")
        else:
            self.canvas.itemconfigure(clickedCell, fill="black")

    #start game/ call generation
    def startGame(self):
        self.stopped = False
        self.generate()
    #stop game
    def stop(self):
        self.stopped = True
    # reset all cells to white and stop game
    def reset(self):
        self.stop()
        for i in range(1,10001):
            currentCell = self.canvas.find_withtag(i)
            self.canvas.itemconfigure(currentCell, fill="white")



    #generates next generation of cells
    def generate(self):
        #for each cell on grid check status of surrounding cells
        for i in range(1,10001):
            aliveCount = 0

            currentCell = self.canvas.find_withtag(i)
            idx = currentCell[0]
            ULCell= self.canvas.find_withtag((idx-101))
            UCell = self.canvas.find_withtag((idx-100))
            URCell = self.canvas.find_withtag((idx-99))
            LCell = self.canvas.find_withtag((idx-1))
            RCell = self.canvas.find_withtag((idx+1))
            LLCell = self.canvas.find_withtag((idx+99))
            LoCell = self.canvas.find_withtag((idx+100))
            LRCell = self.canvas.find_withtag((idx+101))
            ULCellFill = self.canvas.itemcget(ULCell,"fill")
            UCellFill = self.canvas.itemcget(UCell,"fill")
            URCellFill = self.canvas.itemcget(URCell,"fill")
            LCellFill = self.canvas.itemcget(LCell,"fill")
            RCellFill = self.canvas.itemcget(RCell,"fill")
            LLCellFill = self.canvas.itemcget(LLCell,"fill")
            LoCellFill = self.canvas.itemcget(LoCell,"fill")
            LRCellFill = self.canvas.itemcget(LRCell,"fill")

            #get count of alive cells surrounding a center cell
            if(ULCellFill=="black"):
               aliveCount = aliveCount +1
            if(UCellFill=="black"):
                aliveCount = aliveCount +1
            if(URCellFill=="black"):
                aliveCount = aliveCount +1
            if(LCellFill=="black"):
                aliveCount = aliveCount +1
            if(RCellFill=="black"):
                aliveCount = aliveCount +1
            if(LLCellFill=="black"):
                aliveCount = aliveCount +1
            if(LoCellFill=="black"):
                aliveCount = aliveCount +1
            if(LRCellFill=="black"):
                aliveCount = aliveCount +1

        #conways GOL logic for calculating if cell should live or die
            if(self.canvas.itemcget(currentCell, "fill")=="black"):
                if(aliveCount == 2 or aliveCount == 3):
                    self.canvas.itemconfigure(currentCell, fill="black")
                else:
                    self.canvas.itemconfigure(currentCell, fill="white")
            if(self.canvas.itemcget(currentCell, "fill")=="white"):
                if(aliveCount == 3):
                    self.canvas.itemconfigure(currentCell, fill="black")
                else:
                    self.canvas.itemconfigure(currentCell, fill="white")

        #check current gen speed and repeat
        genRate = int(self.genSpeed.get()*1000)
        if not self.stopped:
            self.after(genRate,self.generate)

    #move
    def move_start(self, event):
        self.canvas.scan_mark(event.x, event.y)
    def move_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    #windows zoom
    def zoomer(self,event):
        if (event.delta > 0):
            self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        elif (event.delta < 0):
            self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))

    #linux zoom
    def zoomerP(self,event):
        true_x = self.canvas.canvasx(event.x)
        true_y = self.canvas.canvasy(event.y)
        self.canvas.scale("all", true_x, true_y, 1.1, 1.1)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))
    def zoomerM(self,event):
        true_x = self.canvas.canvasx(event.x)
        true_y = self.canvas.canvasy(event.y)
        self.canvas.scale("all", true_x, true_y, 0.9, 0.9)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))

if __name__ == "__main__":
    root = tk.Tk()
    GameBoard(root).pack(fill="both", expand=True)
    root.mainloop()

