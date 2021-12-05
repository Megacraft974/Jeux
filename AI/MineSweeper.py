from AiMechanics import *
from time import sleep

xGame = 470
yGame = 202
tileSize = 14
xTiles = 16
yTiles = 30
bombs = 99

actualTiles = [0,0]

game = []
for x in range(xTiles):
    game.append([])
    for y in range(yTiles):
        game[x].append((tileSize*x+(tileSize/2)+xGame,tileSize*y+(tileSize/2)+yGame))

typeTiles = []
for x in range(xTiles):
    typeTiles.append([])
    for y in range(yTiles):
        color = getPixel(game[x][y][0],game[x][y][1])
        if color == (0,67,249,255):
            typeTiles[x].append(1)
        elif color == (47,117,13,255):
            typeTiles[x].append(2)
        elif color == (239,62,48,255):
            typeTiles[x].append(3)
        elif color == (0,27,120,255):
            typeTiles[x].append(4)
        elif color == (115,25,18,255):
            typeTiles[x].append(5)
        else:
            bordercolor = getPixel(game[x][y][0],game[x][y][1]+7)
            if bordercolor == (255,255,255,255):
                if color == (0,0,0,255):
                    typeTiles[x].append("f")
                else:
                    typeTiles[x].append("u")
            else:
                typeTiles[x].append(0)
        print("Processing map "+str(((100*x/xTiles)+(100*y/yTiles))/2)+" %")

clickAt(game[0][0][0],game[0][0][1])
clickAt(game[0][0][0],game[0][0][1])

def getNearTiles(actual,typeTiles):
    near = []
    for x in range(2):
        near.append([])
        for y in range(2):
            near.append((typesTiles[x+actual[0]],typesTiles[y+actual[1]]))
    return near

def testRules(near,actual,game):
    unflagged = 0
    flagged = 0
    for x in range(2):
        for y in range(2):
            if near[x][y] == "u":
                unflagged += 1
            elif near[x][y] == "f":
                flagged += 1
    if near[1][1]-flagged == unflagged:
        for x in range(2):
            for y in range(2):
                if near[x][y] == "u":
                    near[x][y] = "cf"
    elif near[1][1] == flagged:
        for x in range(2):
            for y in range(2):
                if near[x][y] == "u":
                    near[x][y] = "cu"
    for x in range(2):
        for y in range(2):
            if near[x][y] == "cf":
                clickAt(game[actual[0]-1+x][actual[1]-1+y][0],game[actual[0]-1+x][actual[1]-1+y][1],Button.right)
            elif near[x][y] == "cu":
                clickAt(game[actual[0]-1+x][actual[1]-1+y][0],game[actual[0]-1+x][actual[1]-1+y][1],Button.left)

def selectTiles(game,xTiles,yTiles,typeTiles):
    global actualTiles
    for x in range(xTiles):
        for y in range(yTiles):
            actualTiles = (x,y)
            near = getNearTiles(actualTiles,typeTiles)
            print("Tested one tile")
            if near[1][1] != "u" and near[1][1] != "f":
                testRules(near,actualTiles,game)

for i in range(10):
    selectTiles(game,xTiles,yTiles,typeTiles)
    print("Checked once")
