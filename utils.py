import random
import pygame as pg
import numpy as np
# from initializers import *
from classes import *

'''
a new state simply means the changed position of the
rectangle and the circle. the rectangle would move according
to the optimal action, the circle falls freely.
'''


def new_state_after_action(s, act):
    updatedPlayer = None

    if act == 2:  # 0 == stay, 1 == left, 2 == right
        if s.player.right + s.player.width > WIDTH:
            rct = s.player
        else:
            rct = pg.Rect(s.player.left + s.player.width, s.player.top, s.player.width,
                          s.player.height)  # Rect(left, top, width, height)
    elif act == 1:  # action is left
        if s.player.left - s.player.width < 0:
            rct = s.player
        else:
            rct = pg.Rect(s.player.left - s.player.width, s.player.top, s.player.width,
                          s.player.height)  # Rect(left, top, width, height)

    else:  # action is 0, means stay where it is
        updatedPlayer = s.player

    s.enemy.top += SPEED
    updatedEnemy = s.enemy
    return State(updatedPlayer, updatedEnemy)


'''
almost similar to a new state, separating because of some easiness
'''


def new_rect_after_action(rect, act):
    if act == 2:  # 0 == left, 1 == right
        if rect.right + rect.width > windowWidth:
            return rect
        else:
            return pg.Rect(rect.left + rect.width, rect.top, rect.width,
                           rect.height)  # Rect(left, top, width, height)
    elif act == 1:  # action is left
        if rect.left - rect.width < 0:
            return rect
        else:
            return pg.Rect(rect.left - rect.width, rect.top, rect.width,
                           rect.height)  # Rect(left, top, width, height)
    else:  # action if to stay
        return rect


'''
defines where the starting x position of the circle
should be while falling.
'''


def circle_falling(crclradius):
    newx = 100 - crclRadius
    multiplier = random.randint(1, 8)  # make more channel by making it a floating point number
    newx *= multiplier
    return newx


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