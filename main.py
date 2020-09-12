#!/usr/bin/env python3

import pygame
import json

map_dir = "assets/maps"
map_name = "map00.json"
sprite_dir = "assets/sprites"
sprite_name = "assets/sprite00.png"
sprite_keycolor = (255, 0, 255)
# Eye-searing magenta
scale_factor = 2
# Non-integer values break window initialisation

class Sprite():
    surface = None
    pos = None
    def __init__(self):
        self.surface = pygame.image.load("assets/sprites/sprite00.png")
        self.surface.convert()
        self.surface.set_colorkey(pygame.Color(*sprite_keycolor))
        self.pos = (8, 6)
        pass

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
    canvas_size = canvas_width, canvas_height = 320, 240
    window_size = (canvas_width * scale_factor, canvas_height * scale_factor)
    # 20x15 tiles when tiles are 16px x 16px
    screen = pygame.display.set_mode(window_size)
    canvas = pygame.Surface(canvas_size)
    canvas.convert()

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

    # Draw tiles to tilemap surface
    for tile_index in range(len(tilemap.tile_ids)):
        tilecoord = (tile_index % tilemap.board_width,
                     tile_index // tilemap.board_width)
        tilemap.surface.blit(tilegfx[tilemap.tile_ids[tile_index] - 1],
                             (tilecoord[0] * tile_width,
                              tilecoord[1] * tile_height))
        # Tiled is sort of 1-indexed because 0 is the built-in blank tile

    sprite = Sprite()
    clock = pygame.time.Clock()

    while(True):
        clock.tick(60)
        for event in pygame.event.get():
            if(event.type == pygame.QUIT or
               event.type == pygame.KEYDOWN and
               event.key == pygame.K_ESCAPE):
                exit()
            if(event.type == pygame.MOUSEBUTTONDOWN):
                if(event.button == 1): # Left mouse click
                    sprite.pos = (event.pos[0] // (tile_width * scale_factor),
                                  event.pos[1] // (tile_height * scale_factor))
                if(event.button == 3): # Right mouse click
                    print(event.pos)
        canvas.blit(tilemap.surface, (0,0))
        canvas.blit(sprite.surface, (sprite.pos[0] * tile_width,
                                     sprite.pos[1] * tile_height))
        pygame.transform.scale(canvas, window_size, screen)
        # Scales canvas onto screen
        pygame.display.flip()
        # Updates the screen, very important

if(__name__ == "__main__"):
    main()
