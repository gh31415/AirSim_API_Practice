import sys

import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('mouse ctrl')
screen.fill((0, 0, 0))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # >------>>>  处理鼠标事件   <<<------< #
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("Mouse Down: ", event)
        if event.type == pygame.MOUSEBUTTONUP:
            print("Mouse Up", event)
        if event.type == pygame.MOUSEMOTION:
            print("Mouse is moving now: ", event)

        # >------>>>  处理键盘事件   <<<------< #
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print("keyboard event: ", event)
