#!/usr/bin/env python3

import pygame
import json

map_dir = "assets/maps"
map_name = "map00.json"

class TileMap():
    tile_ids = None
    board_width = None
    tile_width = None
    tile_height = None
    tileset_path = None
    keycolor = None
    tileset_columns = None
    tileset_tilecount = None
    surface = None
    def __init__(self):
        # Mostly just to keep the file object out of scope
        mapfile = open(f"{map_dir}/{map_name}")
        attribute_tree = json.load(mapfile)
        self.tile_ids = attribute_tree["layers"][0]["data"]
        self.board_width = attribute_tree["width"]
        self.board_height = attribute_tree["height"]
        self.tile_width = attribute_tree["tilewidth"]
        self.tile_height = attribute_tree["tileheight"]
        self.tileset_path = attribute_tree["tilesets"][0]["image"]
        self.keycolor = attribute_tree["tilesets"][0]["transparentcolor"]
        self.tileset_columns = attribute_tree["tilesets"][0]["columns"]
        self.tileset_tilecount = attribute_tree["tilesets"][0]["tilecount"]
        self.surface = pygame.Surface((self.board_width * self.tile_width,
                                       self.board_height * self.tile_height))
        self.surface.convert()
        mapfile.close()

def main():
    pygame.init()
    window_size = w_width, w_height = 320, 240
    # 20x15 tiles when tiles are 16px x 16px
    screen = pygame.display.set_mode(window_size)

    tilemap = TileMap()
    tile_width = tilemap.tile_width
    tile_height = tilemap.tile_height

    tilesheet = pygame.image.load(f"{map_dir}/{tilemap.tileset_path}")
    tilesheet.convert()
    # Make sure the image being used does *not* have an alpha channel
    # or color keying won't work.
    tilesheet.set_colorkey(pygame.Color(tilemap.keycolor))

    # Slice tilesheet into an array of tiles
    tilegfx = []
    for tile_id in range(tilemap.tileset_tilecount):
        tilecoord = (tile_id % tilemap.tileset_columns,
                     tile_id // tilemap.tileset_columns)
        # This is kind of silly when the tileset is only one row
        tile_px_pos = (tilecoord[0] * tile_width, tilecoord[1] * tile_height)
        tilegfx.append(tilesheet.subsurface(pygame.Rect(*tile_px_pos,
                                                        tile_width,
                                                        tile_height)))

    # Draw tiles to screen
    for tile_index in range(len(tilemap.tile_ids)):
        tilecoord = (tile_index % tilemap.board_width,
                     tile_index // tilemap.board_width)
        tilemap.surface.blit(tilegfx[tilemap.tile_ids[tile_index] - 1],
                             (tilecoord[0] * tile_width,
                              tilecoord[1] * tile_height))
        # Tiled is sort of 1-indexed because 0 is the built-in blank tile
    clock = pygame.time.Clock()
    screen.blit(tilemap.surface, (0,0))
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
