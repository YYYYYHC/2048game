import sys

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

    init_state = np.array([[1024, 1024, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], dtype=int)
    nsm = NumSquareMap(element_image_lt, (0, 0), init_state=init_state)

    screen.blit(background, (0, 0))
    nsm.init_game()
    paint_state(screen, nsm)

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    nsm.move_and_put('right')
                if event.key == K_LEFT:
                    nsm.move_and_put('left')
                if event.key == K_UP:
                    nsm.move_and_put('up')
                if event.key == K_DOWN:
                    nsm.move_and_put('down')
        if nsm.game_over():
            game_over(screen, gameover)
        elif nsm.game_win():
            game_win(screen, gamewin)
        else:
            paint_state(screen, nsm)
        pygame.display.update()
        pygame.time.delay(100)


if __name__ == "__main__":
    main()