#!/usr/bin/env python3

import pygame

def main():
    pygame.init()
    window_size = w_width, w_height = 320, 240

    screen = pygame.display.set_mode(window_size)

    while(True):
        for event in pygame.event.get():
            if(event.type == pygame.QUIT or
               event.type == pygame.KEYDOWN and
               event.key == pygame.K_ESCAPE):
                exit()

if(__name__ == "__main__"):
    main()
