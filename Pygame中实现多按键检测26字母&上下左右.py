import sys
import pygame

pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('keyboard ctrl')
screen.fill((0, 0, 0))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    keys = pygame.key.get_pressed()
    for i in range(26):
        if keys[pygame.K_a + i]:  # 检测从 A 到 Z 的按键
            print(chr(pygame.K_a + i))

    # 检测上下左右键
    if keys[pygame.K_UP]:
        print("Up arrow")
    if keys[pygame.K_DOWN]:
        print("Down arrow")
    if keys[pygame.K_LEFT]:
        print("Left arrow")
    if keys[pygame.K_RIGHT]:
        print("Right arrow")

    # 按下 'Esc' 退出程序
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()
