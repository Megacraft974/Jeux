from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
from PIL import ImageGrab,ImageStat
from time import sleep

keyboard = KeyboardController()
mouse = MouseController()

def leftClick(time=0.1):
    mouse.press(Button.left)
    sleep(time)
    mouse.release(Button.left)

def rightClick(time=0.1):
    mouse.press(Button.right)
    sleep(time)
    mouse.release(Button.right)

def moveMouse(x,y):
    mouse.move(x,y)

def scrollMouse(x,y):
    mouse.scroll(x,y)

def clickAt(x,y,button=Button.left):
    mouse.position = (x,y)
    mouse.press(button)

def getMousePos(timer=3):
    while timer > 0:
        print(timer)
        timer -= 1
        sleep(1)
    return mouse.position

def getPixel(x,y):
    px = ImageGrab.grab().load()
    return px[x, y]

def detectSquare():
    pos1 = getMousePos()
    px = ImageGrab.grab()
    colPos1 = px.getpixel(pos1)
    firstSize = px.getbbox()
    px = px.crop((int(pos1[0]),int(pos1[1]),firstSize[2],firstSize[3]))
    size = px.getbbox()
    for x in range(size[2]):
        if px.getpixel((x,0)) != colPos1:
            pos2 = [x]
            print(px.getpixel((x,0)))
            print(x)
            print(pos1)
            print(firstSize)
            print((int(firstSize[2]-pos1[0]),int(firstSize[3]-pos1[1])))
            break
    for y in range(size[3]):
        if px.getpixel((0,y)) != colPos1:
            pos2.append(y)
            break
    pos2 = (pos1[0]+pos2[0],pos1[1]+pos2[1])
    return pos1, pos2
    
