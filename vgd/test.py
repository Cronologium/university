import os

import pygame


ASSETS_ROOT = os.path.join('assets', 'experiments', 'spaceArt', 'png')
LOGO_FILE = os.path.join(ASSETS_ROOT, 'life.png')

TEST_IMAGE = os.path.join(ASSETS_ROOT, 'laserRedShot.png')

HEIGHT = 1080
WIDTH = 1920

def main():
    pygame.init()
    logo = pygame.image.load(LOGO_FILE)
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Test program")

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    image = pygame.image.load(TEST_IMAGE)
    x = 0
    y = 0
    x_mul = 1
    y_mul = 1

    running = True
    index = 0

    while running:
        for event in pygame.event.get():
            screen.blit(image, (x, y))
            pygame.display.flip()

            x += x_mul
            y += y_mul

            if x == WIDTH - 1 or x == 0:
                x_mul *= -1
            if y == HEIGHT - 1 or y == 0:
                y_mul *= -1
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                print(event.key)
                print("{0}: You pressed {1:c}".format(index, event.key))
            elif event.type == pygame.KEYUP:
                print("{0}: You released {1:c}".format(index, event.key))
            index += 1


if __name__ == "__main__":
    main()