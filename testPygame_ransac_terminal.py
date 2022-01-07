import copy
import sys
import os
import time

import numpy as np
import pygame
from pygame.locals import *
from gameobj import NumSquareMap, paint_state
SquareSize = 4

def game_over(screen, gameover):
    screen.blit(gameover, (0, 0))

def game_win(screen, gamewin):
    screen.blit(gamewin, (0, 0))

def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 400))
    background = pygame.image.load('../2048game/resources/background.png').convert()
    gameover = pygame.image.load('../2048game/resources/gameover.png').convert()
    gamewin = pygame.image.load('../2048game/resources/gamewin.png').convert()
    element_image_lt = []
    base_pos = (0, 0)
    square_size = 50

    for i in [2**x for x in range(12)]:
        if i == 1:
            i = 0
        image_file = "./resources/element_" + str(i) + '.png'
        surface = pygame.image.load(image_file).convert()
        surface = pygame.transform.scale(surface, (100, 100))
        element_image_lt.append(surface)

    background = pygame.transform.scale(background, (400, 400))
    gameover = pygame.transform.scale(gameover, (400, 400))
    gamewin = pygame.transform.scale(gamewin, (400, 400))

    # init_state = np.array([[1024, 1024, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], dtype=int)
    nsm = NumSquareMap(element_image_lt, (0, 0))

    screen.blit(background, (0, 0))
    nsm.init_game()
    paint_state(screen, nsm)

    nsm_state_past = nsm.state.copy()
    while 1:
        if nsm.game_over():
            print("over")
            print(nsm.state)
            break
        elif 1: #(nsm_state_past != nsm.state).any()
            nsm_state_lt = ransacsolve(nsm,0)
            if nsm_state_lt == -1:
                nsm.move_and_put(map_dir(np.random.randint(0,4)))
                print("1")
                continue
            for a_nsm_state in nsm_state_lt:
                nsm.change_state(a_nsm_state)
                nsm_state_past = nsm.state.copy()
                paint_state(screen,nsm)
                pygame.display.update()
                pygame.time.delay(100)
                if nsm.game_over():
                    print(nsm.state)
                    print("over")
                    break
        else:

            ransacsolve(nsm,1)

    if nsm.game_over():
        while(1):
            paint_state(screen,nsm)

def map_dir(i):
    if i == 0:
        return 'right'
    if i == 1:
        return 'down'
    if i == 2:
        return 'left'
    if i == 3:
        return 'up'

def getlist(num, snum):
    re_lt = []
    for i in range(snum):
        re_lt.append(num%snum)
        num = num//snum
    return re_lt


def ransacsolve(nsm, flag):
    print("solve a time")
    time.sleep(0.01)
    #random step
    # ini_score = nsm.judge_score()
    ini_state = nsm.state.copy()
    iteration_count = 0
    thread = 0
    nsm_state_lt_return = []
    step_lt__return = []

    if flag == 0:
        for step_num in range(pow(4,3)):
            # print(nsm.state)
            nsm.change_state(ini_state)
            cur_score = 0
            nsm_state_lt = []
            random_step_4 = getlist(step_num, 3)
            print(random_step_4)
            for i in random_step_4:
                dir = map_dir(i)
                nsm.move_and_put(dir)
                nsm_state_lt.append(nsm.state.copy())
                if nsm.game_over():
                    cur_score = -1
                    break
            iteration_count += 1
            #judge score
            if np.sum(nsm.judge_score()) > thread:
                thread = np.sum(nsm.judge_score())
                nsm_state_lt_return = nsm_state_lt
                step_lt__return = random_step_4
        if(thread > 0):
            return nsm_state_lt_return, step_lt__return
        else:
            return -1


    else:
        dir = map_dir(np.random.randint(0,4))
        nsm.move_and_put(dir)
        return



if __name__ == "__main__":
    main()
