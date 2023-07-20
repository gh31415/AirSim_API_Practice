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

    scan_wrapper = pygame.key.get_pressed()
    print("pressed keys is ", scan_wrapper)

    # press 'Esc' to quit
    if scan_wrapper[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()

