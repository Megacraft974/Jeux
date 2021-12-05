from __future__ import division
import os
import pygame
from math import tan, radians, degrees, copysign
from pygame.math import Vector2

class Walls:
    def __init__(self,fenSize):
        self.size = Vector2(64,64)
        self.wallPos = []
        for i in range(int(fenSize.x/self.size.x)):
            self.wallPos.append(Vector2(i*64,-64))
            self.wallPos.append(Vector2(i*64,fenSize.y))
        for i in range(int(fenSize.y/self.size.y)):
            self.wallPos.append(Vector2(-64,i*64))
            self.wallPos.append(Vector2(fenSize.x,i*64))
        
class Car:
    def __init__(self, x, y, fenSize, angle=0.0, length=4, max_steering=30, max_acceleration=5.0):
        self.position = Vector2(x/32, y/32)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.max_velocity = 20
        self.brake_deceleration = 10
        self.free_deceleration = 2

        self.acceleration = 0.0
        self.steering = 0.0

        self.size = Vector2(128/2,64/2)
        self.fenSize = Vector2(fenSize)
        
    def update(self, dt, wallsPos, wallSize):
        self.corner = [self.position*32 + Vector2(self.size.x,self.size.y).rotate(-self.angle), self.position*32 + Vector2(self.size.x,-self.size.y).rotate(-self.angle), self.position*32 + Vector2(-self.size.x,self.size.y).rotate(-self.angle), self.position*32 + Vector2(-self.size.x,-self.size.y).rotate(-self.angle)]

        for c in range(len(self.corner)):
            for w in range(len(wallsPos)):
                if self.corner[c].x > wallsPos[w].x and self.corner[c].x < wallsPos[w].x + wallSize.x and self.corner[c].y > wallsPos[w].y and self.corner[c].y < wallsPos[w].y + wallSize.y:
                    if self.velocity.x > 0:
                        self.velocity.x =  -self.velocity.x - 1
                    elif self.velocity.x < 0:
                        self.velocity.x =  -self.velocity.x + 1

        if not int(self.position.x * 32) in range(10,int(self.fenSize.x+10)) or not int(self.position.y * 32) in range(10,int(self.fenSize.y+10)):
            self.position = Vector2(self.fenSize/64)
            self.velocity = Vector2(0,0)
        
        self.velocity += (self.acceleration * dt, 0)
        self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))
        if self.steering:
            turning_radius = self.length / tan(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0
                    
        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("AI Car Test")
        self.width = 1280#100 -> ??
        self.height = 720#56,25
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False
        self.ppu = 32
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.image_path = os.path.join(self.current_dir, "wall.png")
        self.wall_image = pygame.image.load(self.image_path)
        self.image_path = os.path.join(self.current_dir, "car.png")
        self.car_image = pygame.image.load(self.image_path)
        self.car = Car(self.width/2, self.height/2, (self.width, self.height))
        self.walls = Walls(Vector2(self.width, self.height))
        self.keys = []

    def runFrame(self):
            dt = self.clock.get_time() / 1000
            
            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            # User input
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_z] == 1 or "z" in self.keys:
                if self.car.velocity.x <= 1:
                    self.car.acceleration = self.car.brake_deceleration
                else:
                    self.car.acceleration += 1 * dt
            elif pressed[pygame.K_s] == 1 or "s" in self.keys:
                if self.car.velocity.x >= 1:
                    self.car.acceleration = -self.car.brake_deceleration
                else:
                    self.car.acceleration -= 1 * dt
            elif pressed[pygame.K_SPACE] == 1 or "Space" in self.keys:
                if abs(self.car.velocity.x) > dt * self.car.brake_deceleration:
                    self.car.acceleration = -copysign(self.car.brake_deceleration, self.car.velocity.x)
                else:
                    self.car.acceleration = -self.car.velocity.x / dt
            else:
                if abs(self.car.velocity.x) > dt * self.car.free_deceleration:
                    self.car.acceleration = -copysign(self.car.free_deceleration, self.car.velocity.x)
                else:
                    if dt != 0:
                        self.car.acceleration = -self.car.velocity.x / dt
            self.car.acceleration = max(-self.car.max_acceleration, min(self.car.acceleration, self.car.max_acceleration))
            if pressed[pygame.K_d] == 1 or "d" in self.keys:
                self.car.steering -= 30 * dt
            elif pressed[pygame.K_q] == 1 or "q" in self.keys:
                self.car.steering += 30 * dt
            else:
                self.car.steering = 0
            self.car.steering = max(-self.car.max_steering, min(self.car.steering, self.car.max_steering))

            # Logic
            self.car.update(dt, self.walls.wallPos, self.walls.size)

            # Drawing
            self.screen.fill((0, 0, 0))
            rotated = pygame.transform.rotate(self.car_image, self.car.angle)
            rect = rotated.get_rect()
            self.screen.blit(rotated, self.car.position * self.ppu - (rect.width / 2, rect.height / 2))
            for w in range(len(self.walls.wallPos)): 
                rotated = pygame.transform.rotate(self.wall_image, 0)
                self.screen.blit(rotated, self.walls.wallPos[w])
            pygame.display.flip()
            self.clock.tick(self.ticks)

    def run(self):
        while not self.exit:
            self.runFrame()
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
