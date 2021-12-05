#   Petit jeu de Pac-Man
#       Par William
#
#A faire:
# -Ajout de l'ai des fantomes(aleatoire?)
# -Animations des entités(mouvements)----plus tard
# -Menu principal?
# -Compiler(Distribution?)

from tkinter import *
from math import atan
import random

fen = Tk()
fen.title("Pac-Man sur Python")

CanRun = True

screenSizeX = 720
screenSizeY = screenSizeX

w = "blue"#walls
o = "white"#blank
f = "fakeBlue"#for ghosts ai

labyrinthe = [[w,w,w,w,w,w,f,w,w,w,w,w,w],
              [w,o,o,o,o,w,o,w,o,o,o,o,w],
              [w,o,w,w,o,o,o,o,o,w,w,o,w],
              [w,o,w,w,o,w,w,w,o,w,w,o,w],
              [w,o,o,o,o,o,o,o,o,o,o,o,w],
              [w,w,o,w,o,w,w,w,o,w,o,w,w],
              [f,o,o,w,o,o,o,w,o,w,o,o,f],
              [w,w,o,w,o,w,w,w,o,w,o,w,w],
              [w,o,o,o,o,o,o,o,o,o,o,o,w],
              [w,o,w,w,o,w,w,w,o,w,w,o,w],
              [w,o,w,w,o,o,o,o,o,w,w,o,w],
              [w,o,o,o,o,w,o,w,o,o,o,o,w],
              [w,w,w,w,w,w,f,w,w,w,w,w,w]]

def defineTurns(labyrinthe):
    turns = [[],[]]
    for x in range(1,len(labyrinthe)-1):
        for y in range(1,len(labyrinthe[0])-1):
            counter = []
            if labyrinthe[x][y] == "white":
                for i in ((1,0),(-1,0),(0,1),(0,-1)):
                    if labyrinthe[x+i[0]][y+i[1]] == "white":
                        counter.append(i)
                if len(counter) >= 3 or len(counter) == 1:
                    turns[0].append((x,y))
                    turns[1].append(counter)
                if counter in ([(1,0),(0,1)],[(1,0),(0,-1)],[(-1,0),(0,1)],[(-1,0),(0,-1)]):
                    turns[0].append((x,y))
                    turns[1].append(counter)
    #print(turns)
    return turns

def showTurns(maze, turns, color):
    for i in turns[0]:
        maze[i[0]][i[1]] = color

turns = defineTurns(labyrinthe)
#showTurns(labyrinthe, turns, "pink")

pX = int(len(labyrinthe)/2)
pY = int(len(labyrinthe)/2)+2
pDir = (0,0)

step = screenSizeX/len(labyrinthe)

ghosts = []
GhostSpawn = 6,6
ghostColor = ["red","blue","pink","orange"]

speeds = [10,13,0]#[Player speed, Ghosts speed,speedCounter]

class Ghosts():
    def __init__(self,spawn,velocity):
        self.x,self.y = spawn
        self.dir = (0,-1)

    def move(self,playerX,playerY,maze):
        opp=playerY-self.x+(len(maze)/2)
        adj=playerX-self.y+(len(maze)/2)
        angle = atan(opp/adj)
        acc = (0,0)
        if self.x>playerX:
            angle=angle+180
        if angle < -135:
            acc = (0,1)
        elif angle < -45:
            acc = (-1,0)
        elif angle < 45:
            acc = (0,-1)
        elif angle < 135:
            acc = (1,0)
        elif angle > 135:
            acc = (0,1)
        if randrange(0,5) == 0:
            acc = (acc[0]*(-1),acc[1]*(-1))
        if maze[self.x+acc[0]][self.y+acc[1]] == "blue":
            acc = (0,0)
        return self.x + acc[0],self.y + acc[1]

    def pathFinding(self,maze):
        maze[pX][pY] == "player"
        FGH = []
        iti = []

        for x in range(len(maze)):
            FGH.append([])
            for y in range(len(maze[0])):
                FGH[x].append(abs(pX-x)**2 + abs(pY-y)**2)
                if maze[x][y] == "blue":
                    FGH[x][y] = 1000
                    
        while len(iti)<len(maze)**2:
            psb = 1000
            for dir in [(0,1),(0,-1),(1,0),(-1,0)]:
                if FGH[self.x+dir[0]][self.y-dir[1]] < psb:
                    psb = FGH[self.x+dir[0]][self.y-dir[1]]
            iti.append(dir)
            if FGH[self.x+dir[0]][self.y-dir[1]] == "player":
                break
        print(iti)
        #return iti
        
    def randomAi(self,maze):
        direction = [(0,1),(0,-1),(1,0),(-1,0)]
        for i in direction:
            #print(i)
            if self.x < len(maze)-1 and self.y < len(maze[0])-1:
                if maze[self.x+i[0]][self.y+i[1]] == "blue":
                    direction.remove(i)
        print(maze[self.x+self.dir[1]][self.y+self.dir[0]])
        if maze[self.x+self.dir[0]][self.y+self.dir[1]] == "blue":
            self.dir = random.choice(direction)
        self.x += self.dir[0]
        self.y += self.dir[1]
        print (self.dir,self.x,self.y)
        return self.x,self.y

    def halfRandomAi(self,maze,turns):
        if (self.x,self.y) in turns[0]:
            #print((self.dir[0]*-1+self.x,self.dir[1]*-1+self.y))
            dirs = turns[1][turns[0].index((self.x,self.y))]
            #dirs.remove((self.dir[0]*-1+self.x,self.dir[1]*-1+self.y))
            self.dir = random.choice(dirs)
        #print(self.dir)
        self.x += self.dir[0]
        self.y += self.dir[1]
        return self.x,self.y,self.dir

    def oppositeHalfRandomAi(self,maze,turns):
        a=0

def Pressed_Key(event,maze):
    global pX,pY,pDir
    key = event.char
    #print(pX,pY)
    if key == 'z' and maze[pX][pY-1]!= "blue":
        pDir = (0,-1)
    elif key == 's' and maze[pX][pY+1]!= "blue":
        pDir = (0,1)
    elif key == 'q' and maze[pX-1][pY]!= "blue":
        pDir = (-1,0)
    elif key == 'd' and maze[pX+1][pY]!= "blue":
        pDir = (1,0)

class animate():
    def __init__(self):
        self.anims = []
        self.maxAnims = 4

    def setNew(self,data):
        self.anims.append(data)
        if len(self.anims) > self.maxAnims:
            self.anims.pop(0)
        
    def updateFrame(self,frame):
        for a in self.anims:
            pos = can1.coords(a[0])
            posX,posY = pos[0],pos[1]
            step = a[1][2]
            factor = 0
            #factor = (step/a[2][1])*(frame%a[2][1])
            x,y = a[1][0][0],a[1][1][0]
            x1,y1 = x,y
            #print(x1,y1,posX,posY)
            #print(factor)
            if a[1][3] == (1,0):
                x1 = x+factor
                #print("x+")
            elif a[1][3] == (-1,0):
                x1 = x-factor
                #print("x-")
            elif a[1][3] == (0,1):
                y1 = y+factor
                #print("y+")
            elif a[1][3] == (0,-1):
                y1 = y-factor
                #print("y-")
            x2,y2 = x1+step*0.8,y1+step*0.8
            can1.coords(a[0],x1,y1,x2,y2)
            
def mainloop(ghosts,maze,turns,speeds,anim):
    global pX,pY,pDir
    if CanRun:
        animations = []
        #print(pX,pY)
        speeds[2] +=1
        if speeds[2] % speeds[0] == 0:
            if maze[pX + pDir[0]][pY + pDir[1]]!= "blue":
                pX = pX + pDir[0]
                pY = pY + pDir[1]
            if pX <= 0:
                pX = 11
            elif pX >= 12:
                pX = 1
            elif pY <= 0:
                pY = 11
            elif pY >= 12:
                pY = 1
            #can1.coords(player,pX*step+step*0.1,pY*step+step*0.1,pX*step+step*0.9,pY*step+step*0.9)
            animPx = (pX*step+step*0.1,pX*step+step*0.9)
            animPy = (pY*step+step*0.1,pY*step+step*0.9)
            anim.setNew([player,(animPx,animPy,step,pDir),(speeds[2],speeds[0])])
            #a[entity,((pX,pX+step),(pY,pY+step),step, pdirection),(currentFrame,entitySpeed)]
            #  a[0]    a[1][0][0:1] a[1][1][0:1] a[1][2] a[1][3]     a[2][0]     a[2][1]
        elif speeds[2] % speeds[1] == 0:
            for g in range(4):
                ghostX,ghostY,gDir = ghosts[g][0].halfRandomAi(maze,turns)
                #can1.coords(ghosts[g][1],ghostX*step+step*0.1,ghostY*step+step*0.1,ghostX*step+step*0.9,ghostY*step+step*0.9)
                animPx = (ghostX*step+step*0.1,ghostX*step+step*0.9)
                animPy = (ghostY*step+step*0.1,ghostY*step+step*0.9)
                anim.setNew([ghosts[g][1],(animPx,animPy,step,gDir),(speeds[2],speeds[1])])
        for a in animations:
            a[2]=(speeds[2],a[2][1])
        anim.updateFrame(speeds[2])
        fen.after(30,mainloop,ghosts,maze,turns,speeds,anim)

def Draw_Maze(maze,can,step):
    for x in range(len(maze)):
        for y in range(len(maze[0])):
            if maze[x][y] in ("blue","white","pink"):
                case = can.create_rectangle(x*step,y*step,x*step+step,y*step+step,fill=maze[x][y])
            elif maze[x][y] == "fakeBlue":
                case = can.create_rectangle(x*step,y*step,x*step+step,y*step+step,fill="white")
 
can1 = Canvas(fen,height=screenSizeY,width=screenSizeX)
can1.pack()
fen.bind('<Key>',lambda event : Pressed_Key(event,labyrinthe))
Draw_Maze(labyrinthe,can1,step)
for g in range(4):
    ghosts.append([])
    ghosts[g].append(Ghosts(GhostSpawn,1))
    ghosts[g].append(can1.create_oval(0,0,0,0,fill=ghostColor[g]))
player = can1.create_oval(pX,pY,pX,pY,fill="yellow")
anim = animate()
mainloop(ghosts,labyrinthe,turns,speeds,anim)
fen.mainloop()
CanRun = False
