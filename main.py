#!/usr/bin/env python3

import pygame
import json

map_dir = "assets/maps"

def loadmap():
    # Mostly just to keep the file object out of scope
    mapfile = open(f"{map_dir}/map00.json")
    tilemap = json.load(mapfile)
    tile_ids = tilemap["layers"][0]["data"]
    board_width = tilemap["width"]
    mapfile.close()
    return tile_ids, board_width
    pass

def main():
    pygame.init()
    window_size = w_width, w_height = 320, 240
    # 20x15 tiles when tiles are 16px x 16px
    screen = pygame.display.set_mode(window_size)

    tile_ids, board_width = loadmap()
    tilesheet = pygame.image.load(f"{map_dir}/tilesets/tileset00.png")
    tilesheet.convert()
    # Make sure the image being used does *not* have an alpha channel
    # or color keying won't work.
    tilesheet.set_colorkey(pygame.Color(255,0,255))
    # Eye-searing magenta

    tilegfx = []

    tilegfx.append(tilesheet.subsurface(pygame.Rect(0,0,16,16)))
    tilegfx.append(tilesheet.subsurface(pygame.Rect(16,0,16,16)))
    tilegfx.append(tilesheet.subsurface(pygame.Rect(32,0,16,16)))
    tilegfx.append(tilesheet.subsurface(pygame.Rect(48,0,16,16)))
    # TODO: Make this into a loop

    for tile_index in range(len(tile_ids)):
        tilecoord = (tile_index % board_width,
                     tile_index // board_width)
        screen.blit(tilegfx[tile_ids[tile_index] - 1],
                            (tilecoord[0] * 16, tilecoord[1] * 16))
        # Tiled is sort of 1-indexed because 0 is the built-in blank tile
    print(tilecoord)
    clock = pygame.time.Clock()
    pygame.display.flip()
    # Updates the screen, very important

    while(True):
        clock.tick(60)
        for event in pygame.event.get():
            if(event.type == pygame.QUIT or
               event.type == pygame.KEYDOWN and
               event.key == pygame.K_ESCAPE):
                exit()

if(__name__ == "__main__"):
    main()
