import CarSimulator


class CarDriver:
    def __init__(self):
        env = CarSimulator.Game()

    def run(self):
        while not env.exit:
            env.runFrame()
        CarSimulator.pygame.quit()

class Entity:
    def __init__(self,params,inputs):
        self.settings = params
        self.input = inputs
        self.wallSide = self.input[5] - self.input[4]
    def run(self):
        for i in range(len(settings)):
            if settings[i][0] == 0:
                

class Builder:
    def __init__(self,pop):
        self.entity = []
        Input = ["posX","posY","Speed","Direction","WallDirection","WallDistance"]
        Layer1 = ["WallSide","WallFront","CanBrake"]
        Output = ["Z","S","Q","D","Space"]
        
