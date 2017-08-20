# -*- coding: utf-8 -*-
"""
Created on Thu June 17 22:54:41 2017

@author: Stroom
"""

"""""
## DESCRIPTION ##

'Break The Brain'

This is a game where played is needed to choose right color, which displayed word means.
For example, on the screen will be word 'GREEN' (this word can be any color) which painted pink color.
In the bottom of the screen will be shown some cubes (depending on level their amount can changes).
Supposably we are on first level and we got 4 cubes. Let it have yellow, red, green and blue colors.
Player must click on one of these cubes to make his choice.

1) If he makes right choice (in our example - picking green cube), he will get some points and go next.
2) If he fails, the game will stop.
"""""

import pygame
from pygame import *
from random import randint
from random import choice
from time import clock
from datetime import *

pygame.init()
width = 450; height = 450
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Break The Brain')

colors = {
'transparent': Color("#123456"),
'black': (0, 0, 0),
'white': (255, 255, 255),
'red': (244, 65, 65),
'pink': (244, 66, 131),
'purple': (214, 65, 244),
'blue': (65, 76, 244),
'cyan': (65, 229, 244),
'yellow': (255, 231, 17),
'green': (7, 175, 26),
'brown': (175, 81, 8),
'orange': (255, 140, 33)
        }

#COLORS
transparent = Color("#123456")
black = 0, 0, 0
white = 255, 255, 255
lightgray = 200, 200, 200
gray = 150, 150, 150
darkgray = 100, 100, 100

# BUTTONS
cube0 = Surface((70,70))
cube1 = Surface((70,70))
cube2 = Surface((70,70))
cube3 = Surface((70,70))
cube4 = Surface((70,70))
cube5 = Surface((70,70))

# TIMER
point = Surface((20, 20))
point.fill(colors['black'])

background = Surface((width, height))
screen = Surface((width, 300))
buttons = Surface((width, 100))
timer_surface = Surface((350 ,20))

x = 80 #
x2 = 62 # these constants are correct only
x3 = 52 # with 450x450 window's size
left = 65 #

# FONT
pygame.font.init()
font = pygame.font.SysFont("comicsansms", 80)
font2 = pygame.font.SysFont("Chiller", 65)
font3 = pygame.font.SysFont("Courier New", 28)

def timer():
    global COUNT
    global LIMIT
    point = Surface((20, 20))
    point.fill(colors['black'])
    print(LIMIT//20-COUNT//20)
    for i in range(LIMIT//20-COUNT//20):
        timer_surface.blit(point, (160+30*i+10*((100-LIMIT)//20), 0))
        background.blit(timer_surface, (0, 20))

def generate_colors(amount):
    colors = ['black', 'red', 'pink', 'purple', 'blue', 'cyan', 'yellow', 'green', 'brown', 'orange']
    picked_colors = []
    for i in range(amount):
        color = choice(colors)
        picked_colors += [color]
        colors.remove(color)
    print('PICK: ', picked_colors)
    return picked_colors

def quit():
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.quit()
            break

def l_click():
    if pygame.mouse.get_pressed()[0] == 1:
        coord = pygame.mouse.get_pos()
        return coord[0], coord[1]

def generate_level(cubesNumber):
    lvl = cubesNumber-3
    global side
    if lvl == 1:
        side = 70
        y_pos = 350
    elif lvl == 2:
        side = 60
        y_pos = 355
    elif lvl == 3:
        side = 50
        y_pos = 360

    cubes = [cube0, cube1, cube2, cube3, cube4, cube5]
    global x, x2, x3
    deltas = [x, x2, x3]
    global left
    x_pos = []
    for i in range(cubesNumber):
        coord = left+i*deltas[lvl-1]
        if lvl == 2: coord += 1
        x_pos += [coord]

    global colors_picked
    if not colors_picked:
        picked_colors = generate_colors(cubesNumber)
        answer = choice(picked_colors)                  # answer is one of generated colors
        color = choice(picked_colors)
        global text
        text = font.render(answer, True, colors[color])
        for i in range(cubesNumber):
            current_color = choice(picked_colors)
            cubes[i].fill(colors[current_color])
            picked_colors.remove(current_color)
            if current_color == answer:
                global answer_pos
                answer_pos = x_pos[i]
        print('ANSWER: ', answer) # <
        colors_picked = True

    for i in range(cubesNumber):
        buttons.blit(pygame.transform.scale(cubes[i], (side,side)), (x_pos[i], y_pos-350))

def countdown():
    sec3 = pygame.image.load("./graph/3.png")
    sec2 = pygame.image.load("./graph//2.png")
    sec1 = pygame.image.load("./graph//1.png")
    sec0 = pygame.image.load("./graph//0(0).png")
    sec = [sec3, sec2, sec1, sec0]

    for i in range(4):
        time0 = clock()
        while round(clock() - time0,2) != 1:
            pass
        else:
            background.blit(sec[i], (200, 100))
            window.blit(background, (0, 0))
            pygame.display.update()
            if i == 3:
                pygame.time.delay(250)

def game_scene():
    global COUNT

    global current_scene
    global current_level
    global current_score

    global started
    global colors_picked
    background.fill(white)
    screen.fill(colors['white'])
    buttons.fill(colors['white'])
    timer_surface.fill(colors['white'])
    round_cross = pygame.image.load("./graph/cross.png")
    back = background.blit(round_cross, (410, 10))

    if current_level == 1:
        generate_level(4) # set of buttons for level 1 [amount: 4]
    elif current_level == 2:
        generate_level(5) # set of buttons for level 2 [amount: 5]
    elif current_level == 3:
        generate_level(6) # set of buttons for level 3 [amount: 6]

    window.blit(background, (0, 0))
    background.blit(buttons, (0, 350))
    timer()

    if not started: # state of game_scene
        countdown()
        started = True
        global start_time
        start_time = datetime.now()

    global text
    if text != None: # <
        screen.blit(text, (105+randint(0,5), 80+(randint(0,5))))
        background.blit(screen, (0, 50))

    if l_click() != None:
        print(l_click())
        if back.collidepoint(l_click()):
            current_scene = 'menu'
            started = False
            colors_picked = False
            COUNT = 0
            time = 0
        if started and (350 <= l_click()[1] <= 350 + side):
            global answer_pos
            if (answer_pos <= l_click()[0] <= answer_pos + side):
                print('right')
                current_score += 1
                colors_picked = False
                text = None
                answer_pos = None
                pygame.time.delay(75)
            else:
                global session_time
                finish_time = datetime.now()
                print('start time', start_time)
                print('finish_time', finish_time)
                session_time = finish_time - start_time
                current_scene = 'loss'
                started = False
                colors_picked = False
                print('TOTAL SCORE: ',current_score) #
                print('LOSS')                        #
            COUNT = 0
            time = 0

def game_loss():
    loss = pygame.image.load("./graph/score_board.png")
    pushme_button = pygame.image.load("./graph/pushme_button_166_90.png")
    background.blit(loss, (0, 0))
    global current_score
    global current_level
    global session_time
    answer = font3.render('answers = '+str(current_score), True, colors['black'])
    background.blit(answer, (15, 280))
    level = font3.render('level   x '+str(current_level), True, colors['black'])
    background.blit(level, (15, 315))
    time = font3.render('YOUR TIME:', True, colors['black'])
    background.blit(time, (250, 280))
    time = font3.render(str(session_time)[2:-2], True, colors['black'])
    background.blit(time, (250, 315))
    score = font2.render('TOTAL SCORE = '+str(current_score*current_level), True, colors['black'])
    background.blit(score, (10, 370))
    pushme_bttn = background.blit(pushme_button, (143, 178))

    global set_pos
    if not set_pos:
        pygame.mouse.set_pos(225, 350)
        set_pos = True

    if pushme_bttn.collidepoint(pygame.mouse.get_pos()):
        background.blit((pygame.transform.scale(pushme_button, (199, 108))), (128, 165))
    if l_click() != None:
        if pushme_bttn.collidepoint(l_click()) & set_pos:
            global current_scene
            current_scene = 'menu'
            current_score = 0
            set_pos = False
#143 292
#203 247

def game_menu():
    menu = pygame.image.load("./graph/menu.png")
    play_button = pygame.image.load("./graph/play_button_200x60.png")
    active_play_button = pygame.image.load("./graph/active_play_button_200x60.png")
    level_button = pygame.image.load("./graph/level_button_200x60.png")
    active_level_button = pygame.image.load("./graph/active_level_button_200x60.png")
    credits_button = pygame.image.load("./graph/credits_button_200x60.png")
    active_credits_button = pygame.image.load("./graph/active_credits_button_200x60.png")

    background.blit(menu, (0,0))
    play_bttn = background.blit(play_button, (125, 60))
    levl_bttn = background.blit(level_button, (125, 140))
    crdt_bttn = background.blit(credits_button, (125, 220))

    if play_bttn.collidepoint(pygame.mouse.get_pos()):
        background.blit(active_play_button, (125, 60))
    elif levl_bttn.collidepoint(pygame.mouse.get_pos()):
        background.blit(active_level_button, (125, 140))
    elif crdt_bttn.collidepoint(pygame.mouse.get_pos()):
        background.blit(active_credits_button, (125, 220))

    global current_scene

    if l_click() != None:
        if play_bttn.collidepoint(l_click()):
            current_scene = 'game'
        elif levl_bttn.collidepoint(l_click()):
            current_scene = 'level_menu'
            pygame.time.delay(100)
        elif crdt_bttn.collidepoint(l_click()):
            current_scene = 'credits'


def level_menu():
    level_menu = pygame.image.load("./graph/level_menu.png")
    lvl_1_button = pygame.image.load("./graph/level_1.png")
    active_lvl_1_button = pygame.image.load("./graph/active_level_1_200x60.png")
    lvl_2_button = pygame.image.load("./graph/level_2.png")
    active_lvl_2_button = pygame.image.load("./graph/active_level_2_200x60.png")
    lvl_3_button = pygame.image.load("./graph/level_3.png")
    active_lvl_3_button = pygame.image.load("./graph/active_level_3_200x60.png")

    background.blit(level_menu, (0,0))
    lvl_1_bttn = background.blit(lvl_1_button, (18,44))
    lvl_2_bttn = background.blit(lvl_2_button, (202,199))
    lvl_3_bttn = background.blit(lvl_3_button, (23,333))

    global current_scene
    global current_level

    if lvl_1_bttn.collidepoint(pygame.mouse.get_pos()):
        background.blit(active_lvl_1_button, (18, 44))
        if l_click() != None:
            if lvl_1_bttn.collidepoint(l_click()):
                current_level = 1
                current_scene = 'menu'
                pygame.time.delay(100)
    elif lvl_2_bttn.collidepoint(pygame.mouse.get_pos()):
        background.blit(active_lvl_2_button, (202,199))
        if l_click() != None:
            if lvl_2_bttn.collidepoint(l_click()):
                current_level = 2
                current_scene = 'menu'
                pygame.time.delay(100)
    elif lvl_3_bttn.collidepoint(pygame.mouse.get_pos()):
        background.blit(active_lvl_3_button, (23,333))
        if l_click() != None:
            if lvl_3_bttn.collidepoint(l_click()):
                current_level = 3
                current_scene = 'menu'
                pygame.time.delay(100)

    global LIMIT
    LIMIT = 100 + 20*(1 - current_level)

def credits():
    background.fill((93, 216, 119))
    font3 = pygame.font.SysFont("Chiller", 50)
    text = [' '*2+'"BREAK THE BRAIN"', '', 'created by Stroom', 'stroooooom@gmail.com', '01/08/17']
    for i in range(len(text)):
        t = font3.render(text[i], True, colors['black'])
        background.blit(t, (20, 20 + i*60))

    OK = pygame.image.load("./graph/OK.png")
    OK_bttn = background.blit(OK, (120, 340))
    if OK_bttn.collidepoint(pygame.mouse.get_pos()):
        background.blit((pygame.transform.scale(OK, (238, 97))), (108, 329))
    if l_click() != None:
        if OK_bttn.collidepoint(l_click()):
            global current_scene
            current_scene = 'menu'

COUNT = 0 # timer
LIMIT = 100 # timer's stop

start_time = 0
session_time = 0

current_scene = 'menu'
current_level = 1
current_score = 0

started = False
colors_picked = False

side = None
text = None
answer_pos = None
set_pos = False

while True:
    quit()

    if current_scene == 'menu':
        game_menu()

    elif current_scene == 'game':
        game_scene()
        COUNT += 1
        if COUNT%20 == 0 and COUNT!=LIMIT: # ~ 1 sec (with COUNT += 1 [changed to 2])
            print(COUNT)
        elif COUNT == LIMIT:
            print('timeout') # <
            COUNT = 0
            current_scene = 'loss'

    elif current_scene == 'loss':
        game_loss()

    elif current_scene == 'level_menu':
        level_menu()

    elif current_scene == 'credits':
        credits()

    window.blit(background, (0, 0))
    pygame.display.flip()
    pygame.time.delay(50)
