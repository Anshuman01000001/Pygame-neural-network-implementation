import neat.config
import pygame
import neat
import time
import os
import random
pygame.font.init()
import pymunk
import math

win_height = 500
win_width = 800
Gen = 0
driver = pygame.transform.scale2x(pygame.image.load(os.path.join("Assets","driver-head.png")))
car = pygame.transform.scale2x(pygame.image.load(os.path.join("Assets","car-full.png")))


BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("Assets","lowres-stage-icon-arctic.png")))




class car:
    Velocity = 20

    def __init__(self,space, screen):
        self._space = space
        self._screen = screen
        self.turret_wheel = None
        self.wheels = []
        self.wheel_image = pygame.transform.scale2x(pygame.image.load(os.path.join("Assets","Tire.png")),(64,64))
        self.wheel_offset = (0,0)
        self.body = None
        self.image = None
        self.image_offset = (0,0)
        self.wheel_turn_force = 10000
        self.max_speed = 100
        self.all_wheel_drive = False
    
    def _create_wheel(self,mass,x_pos,y_pos,radius,elasticity=0.1,friction = 0.9):
        inertia = pymunk.moment_for_circle(mass,0,radius,(0,0))
        body = pymunk.Body(mass, inertia, pymunk.Body.DYNAMIC)
        body.position = x_pos, y_pos
        shape = pymunk.Circle(body,radius, (0,0))
        shape.elasticity = elasticity
        shape.friction = friction
        shape.filter = pymunk.ShapeFilter(categories=0b1000)

        self._space.add(body,shape)
        return body, shape
    
    def create_poly(self,mass,x_pos,y_pos,w,h,vs=0,elasticity=0.3,friction=0.9, color=None, rot=0, s_filter=3):
        if vs == 0:
            vs = [(-w/2,-h/2),(w/2,-h/2),(w/2,h/2),(-w/2,h/2)]
        radius = 2.0
        inertia = pymunk.moment_for_poly(mass,vs,(0,0),radius=radius)
        body = pymunk.Body(mass,inertia)
        body.angle = rot
        shape = pymunk.Poly(body,vs,radius=1)
        #shape2 = pm.Circle(body,50,(100,0))
        body.position = x_pos,y_pos

        shape.elasticity = elasticity
        shape.friction = friction
        shape.filter = pymunk.ShapeFilter(categories=s_filter)
        if color:
            shape.color = color
        #shape2.filter = pymunk.ShapeFilter(categories=0b1000)
        self._space.add(body,shape)
        return body,shape
    
    '''''
    def update(self):
        keys = pygame.key.get_pressed()
        # going forward
        if keys[pygame.K_d]:
            # limiting velocity to 500
            if self.wheels[0].velocity.int_tuple[0] < self.max_speed:
                self.wheels[0].apply_force_at_world_point((self.wheel_turn_force, 12), (0, 0))
            # all wheel drive
            if self.all_wheel_drive:
                for i in range(1, len(self.wheels)):
                    if self.wheels[i].velocity.int_tuple[0] < self.max_speed:
                        self.wheels[i].apply_force_at_world_point((self.wheel_turn_force, 12), (0, 0))
        # going backward
        elif keys[pygame.K_a]:
            if self.wheels[0].velocity.int_tuple[0] > -self.max_speed:
                self.wheels[0].apply_force_at_world_point((-self.wheel_turn_force, 12), (0, 0))
            if self.all_wheel_drive:
                for i in range(1, len(self.wheels)):
                    if self.wheels[i].velocity.int_tuple[0] > -self.max_speed:
                        self.wheels[i].apply_force_at_world_point((-self.wheel_turn_force, 12), (0, 0))
    '''

    def draw(self):
        """
        Draws the car body and wheels onto the screen. Limit the x-pos of the car
        to half of the screen width.
        :return: None
        """
        # center coordinates of the car body in pm-space
        car_body_center = self.body.position
        # drawing front and back wheels
        for i in range(len(self.wheels)):
            rot = -math.degrees(self.wheels[i].angle)
            # grab loaded image
            image = pygame.transform.rotate(self.wheel_image, rot)
            center = self.wheels[i].position
            rect = image.get_rect(center=image.get_rect(center=center).center)
            # shift the x-pos of the wheel by (x-cord of the car body) - 400
            if car_body_center[0] > 400 + -self.wheel_offset[0]:
                rect.centerx -= car_body_center[0] - 400 + self.wheel_offset[0]
            # draw the car body onto the screen
            self._screen.blit(image, rect)
        # get rotation of the car body or wheel
        car_body_rot = -math.degrees(self.body.angle)
        # grab loaded image
        image = pygame.transform.rotate(self.image, car_body_rot)
        center = image.get_rect(center=car_body_center).center
        car_body_rect = image.get_rect(center=(center[0]+self.image_offset[0], center[1]+self.image_offset[1]))
        if car_body_rect.centerx > 400:
            car_body_rect.centerx = 400
        # draw the car body onto the screen in front of the wheels
        self._screen.blit(image, car_body_rect)

class hills:
    Velocity = 5
    GAP = 10

class background:
    Velocity = 5

def draw_window(win):
    win.blit(BG_IMG,(0,0))







def run(config_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path)


    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    #winner = p.run(main,50)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config_feedforward.txt")
    run(config_path)
