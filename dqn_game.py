import pygame
import random
import sys
import numpy as np
from pygame.locals import *
from initializers import *
# from utils import *
from classes import *


clock = pygame.time.Clock()

myFont = pygame.font.SysFont("monospace", 35)

'''
a new state simply means the changed position of the
rectangle and the circle. the rectangle would move according
to the optimal action, the circle falls freely.
'''

def new_state_after_action(s, act):
    updatedPlayer = None

    if act == 2:  # 0 == stay, 1 == left, 2 == right
        if s.player.right + s.player.width > WIDTH:
            updatedPlayer = s.player
        else:
            updatedPlayer = pygame.Rect(s.player.left + s.player.width, s.player.top, s.player.width,
                          s.player.height)  # Rect(left, top, width, height)
    elif act == 1:  # action is left
        if s.player.left - s.player.width < 0:
            updatedPlayer = s.player
        else:
            updatedPlayer = pygame.Rect(s.player.left - s.player.width, s.player.top, s.player.width,
                          s.player.height)  # Rect(left, top, width, height)

    else:  # action is 0, means stay where it is
        updatedPlayer = s.player

    s.enemy.top += SPEED
    updatedEnemy = s.enemy
    return State(updatedPlayer, updatedEnemy)


'''
calculate the score based on the relative position of the
circle and the rectangle.
'''


def calculate_score(player, enemy):
    if not (player.left <=  enemy.left <= player.right):  # if the circle'x x position is between the rectangles left and right
        return 1
    else:
        return -1


'''
numpy array can't work with custom objects as indices.
that's why we must create an integer representation of the states
the position of the rectangle and circle combined should give us a unique
identifier. we are storing the value in another dictionary which would hold the unique
indices.
'''


def state_to_number(s):
    r = s.player.left
    c = s.enemy.left
    n = int(str(r) + str(c) + str(s.enemy.top))

    if n in QIDic:
        return QIDic[n]
    else:
        if len(QIDic):
            maximum = max(QIDic, key=QIDic.get)  # Just use 'min' instead of 'max' for minimum.
            QIDic[n] = QIDic[maximum] + 1
        else:
            QIDic[n] = 1
    return QIDic[n]


def get_best_action(s):
    return np.argmax(Q[state_to_number(s), :])

def set_level(score, SPEED):
	if score < 20:
		SPEED = 5
	elif score < 40:
		SPEED = 8
	elif score < 60:
		SPEED = 12
	else:
		SPEED = 15
	return SPEED
	# SPEED = score/5 + 1


def get_best_action(s):
    return np.argmax(Q[state_to_number(s), :])

def draw_player(player):
	pygame.draw.rect(screen, RED, player)

def draw_enemies(enemy):
	pygame.draw.rect(screen, BLUE, enemy)

def update_enemy_positions(enemy_list, score):
	for idx, enemy_pos in enumerate(enemy_list):
		if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
			enemy_pos[1] += SPEED
		else:
			enemy_list.pop(idx)
			score += 1
	return score

def calculate_reward(player, enemy):
	if(player.top <= enemy.bottom <= player.bottom): #if the enemy's y position is between the player's top and bottm
		if not (player.left <=  enemy.left <= player.right):  # if the enemy's x position is between the player's left and right
			reward = 1
		else:
			reward = -1
		enemy.left = random.randint(0,WIDTH-enemy_size)
		enemy.top = 0
	else:
		reward = 0 #if neither collided nor escaped enemy
		enemy.top += SPEED
	return reward

def detect_collision(player_pos, enemy_pos):
	p_x = player_pos[0]
	p_y = player_pos[1]

	e_x = enemy_pos[0]
	e_y = enemy_pos[1]

	if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x+enemy_size)):
		if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y+enemy_size)):
			return True
	return False



while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

	screen.fill(BACKGROUND_COLOR)

	reward = calculate_reward(player, enemy)
	print(reward)

	act = random.randint(0,2) # 0 means stay, 1 means left, 2 means right

	s = State(player, enemy)
	# print(s.enemy)
	# act = get_best_action(s)  # get the best action so far in this state
	# print(act)
	r0 = calculate_reward(s.player, s.enemy) # get the immediate reward of this step
	# print(r0)
	s1 = new_state_after_action(s, act) # new state after taking the best action
	# build the Q table, indexed by (state, action) pair
	Q[state_to_number(s), act] += lr * (r0 + y * np.max(Q[state_to_number(s1), :]) - Q[state_to_number(s), act])

	# score = update_enemy_positions(enemy_list, score)
	# SPEED = set_level(score, SPEED)
	player = s1.player
	enemy = s.enemy


	text = "Score:" + str(score)
	label = myFont.render(text, 1, YELLOW)
	screen.blit(label, (WIDTH-200, HEIGHT-40))

	text = "Deaths:" + str(deaths)
	label = myFont.render(text, 1, RED)
	screen.blit(label, (WIDTH-200, HEIGHT-80))

	draw_enemies(enemy)
	# player = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
	draw_player(player)
	
	if reward == 1:  # got it!
		score += reward  # add the reward to the total score
	elif reward == -1:  # death
		deaths -= reward # add the reward to the death count

	clock.tick(30)

	pygame.display.update()
