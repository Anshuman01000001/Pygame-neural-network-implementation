import neat.config
import pygame
import neat
import time
import os
import random
pygame.font.init()

win_height = 500
win_width = 800
Gen = 0
driver = pygame.transform.scale2x(pygame.image.load(os.path.join("Assets","driver-head.png")))
tire = pygame.transform.scale2x(pygame.image.load(os.path.join("Assets","Tire.png")))
car = pygame.transform.scale2x(pygame.image.load(os.path.join("Assets","car-full.png")))


BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("Assets","lowres-stage-icon-arctic.png")))




class car:
    Velocity = 20

    def __init__(self):
        pass

class wheels:
    Velocity = 20

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
