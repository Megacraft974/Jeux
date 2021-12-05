from time import sleep
from tkinter import *
from math import cos,sin,sqrt
from random import randint

class Chill(object):
    def __init__(self,sizeX=300,sizeY=-1):
        self.x = sizeX
        if sizeY <= 0:
            self.y = int(sizeX*5/3)
        else:
            self.y = sizeY
        self.size = int(sqrt(self.x*self.x + self.y * self.y))

        self.fenPosX = 500
        self.fenPosY = 350

        self.fen = Tk()
        self.fen.title("Chill Game")
        self.fen.geometry(str(self.x)+"x"+str(self.y)+"+"+str(self.fenPosX)+"+"+str(self.fenPosY))

        self.can = Canvas(width = self.x, height = self.y, bg = "white")
        self.can.pack()
        self.can.bind("<Button-1>",self.jump)

        self.playerPosX = 0
        self.playerPosY = 0
        self.JumpHeight = 20
        self.level = 1

    def dot(self,x,y,col='black'):
        self.can.create_rectangle(x,y,x,y,fill=col)

    def square(self,x,y,thick,col='black'):
        self.can.create_rectangle(x,y,x+thick,y+thick,fill=col)

    def half_circle(self,posx,posy,r,facing,col='black'):
        for o in range(360):
            x = cos(o) * r
            y = sin(o) * r
            if facing == "up" and y <= 0:
                self.dot(x+posx,y+posy,col)
            elif facing == "down" and y >= 0:
                self.dot(x+posx,y+posy,col)
            if facing == "left" and x <= 0:
                self.dot(x+posx,y+posy,col)
            elif facing == "right" and x >= 0:
                self.dot(x+posx,y+posy,col)

    def line(self,posx,posy,l,o=0,col="black"):
        o = o*3.14/180
        for r in range(int(l)):
            x = cos(o) * r
            y = sin(o) * r
            self.dot(int(x+posx),int(y+posy),col)

    def circle(self,posx,posy,r,fill=False,col="black"):
        if fill:
            for f in range(int(r)):
                for o in range(360):
                    x = cos(o) * f
                    y = sin(o) * f
                    self.dot(x+posx,y+posy)
        else:
            for o in range(360):
                x = cos(o) * r
                y = sin(o) * r
                self.dot(x+posx,y+posy)

    def resetScreen(self):
        self.can.delete(ALL)

    def drawMap(self,mapDraw,x,y,step,posPlayer):
        self.resetScreen()
        for d in range(int(posPlayer),len(mapDraw)):
            if mapDraw[d] == "floor":
                self.line(x,y,step)
            elif mapDraw[d] == "hole":
                try:
                    if mapDraw[d-1] == "floor":
                        self.line(x,y,step/2,90)
                    if mapDraw[d+1] == "floor":
                        self.line(x+step,y,step/2,90)
                except:
                    d = d
            x += step

    def player(self,x,y,s,state=""):
        self.half_circle(x+s,y,s,"up")#Tete
        self.half_circle(x,y,s,"down")#TCorp)s
        self.half_circle(x,y+s/4,s/4,"down")#Aile
        self.line(x-s,y,s)#Corps(haut)
        self.line(x+s,y,s)#Tete(bas)
        self.line(x-s,y,s,225)#Queue
        self.line(x,y+s,s,90)#Patte
        self.circle(x+s,y-s/2,s/10,True)#Oeil

    def mapGeneration(self,mapSize,difficulty):
        self.map = ["floor"]
        for m in range(mapSize):
            for w in range(randint(2,10-difficulty)):
                self.map.append("floor")
            for h in range(randint(0,difficulty+int(m/5))):
                self.map.append("hole")
        return self.map
    
    def jump(self,event):
        self.playerPosY += self.JumpHeight

    def frame(self,mapDraw,progress):
        self.drawMap(mapDraw,0,int(self.y/2),20,progress)
        self.player(int(self.x/4/20)*20,int(self.y/2)-20 - self.playerPosY,10)
        if self.playerPosY >= self.JumpHeight:
            self.playerPosY -= self.JumpHeight
        self.can.update()
    
def play():
    game = Chill()
    mapDraw = game.mapGeneration(100,2)
    for p in range(0,100):
        game.frame(mapDraw,p)

play()
