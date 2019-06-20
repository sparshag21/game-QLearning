import numpy as np
import pygame
import random 

#initializing parameters

WIDTH = 800
HEIGHT = 600

RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
BACKGROUND_COLOR = (0,0,0)

player_size = 50
player_pos = [WIDTH/2, HEIGHT-player_size]
playerstep = 20
player = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)

enemy_size = 50
enemy_pos = [random.randint(0,WIDTH-enemy_size), 0]
enemy = pygame.Rect(enemy_pos[0], enemy_pos[1], enemy_size, enemy_size)
enemy_list = [enemy]

SPEED = 20

#Initializing Q-values and setting number of states and actions
QIDic = {}

states = int(WIDTH/player_size*(WIDTH-enemy_size)/enemy_size*HEIGHT/SPEED)
action_number = 3

Q = np.zeros(
[states, action_number])

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

#Initializing score and reward 
game_over = False

reward = 0
score = 0
deaths = 0

# set learning rate
lr = .85
y = .99