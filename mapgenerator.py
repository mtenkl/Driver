import csv
from numpy.lib.shape_base import tile
import pygame
import numpy as np


class MapGenerator():

    def __init__(self, map_data_path) -> None:

        self._TILE_SIZE = 256
        self._roadEW = pygame.image.load("images/roadEW.tga")
        self._roadNE = pygame.image.load("images/roadNE.tga")
        self._roadNEWS = pygame.image.load("images/roadNEWS.tga")
        self._roadNS = pygame.image.load("images/roadNS.tga")
        self._roadNW = pygame.image.load("images/roadNW.tga")
        self._roadPLAZA = pygame.image.load("images/roadPLAZA.tga")
        self._roadSE = pygame.image.load("images/roadSE.tga")
        self._roadSW = pygame.image.load("images/roadSW.tga")
        self._roadNES = pygame.image.load("images/roadNES.tga")
        self._roadWES = pygame.image.load("images/roadWES.tga")
        self._roadWNE = pygame.image.load("images/roadWNE.tga")
        self._roadWNS = pygame.image.load("images/roadWNS.tga")
        self._roadEND = pygame.image.load("images/roadEND.tga")

        self._x_offset = 0
        self._y_offset = 0

        self._world = np.genfromtxt(map_data_path, delimiter=";")
        self._world_padded = np.pad(self._world, 1)

    def _get_tile(self, row, col):

        row += 1
        col += 1

        if self._world_padded[row, col] == 0:
            return self._roadPLAZA
        elif self._world_padded[row, col] == 1:
            # NEWS
            if self._world_padded[row, col-1] == 1 and self._world_padded[row, col+1] == 1 and self._world_padded[row-1, col] == 1 and self._world_padded[row+1, col] == 1:
                return self._roadNEWS
            # EW
            elif (self._world_padded[row, col-1] == 1 or self._world_padded[row, col+1] == 1) and self._world_padded[row-1, col] == 0 and self._world_padded[row+1, col] == 0:
                return self._roadEW
            # NS
            elif self._world_padded[row, col-1] == 0 and self._world_padded[row, col+1] == 0 and (self._world_padded[row-1, col] == 1 or self._world_padded[row+1, col] == 1):
                return self._roadNS
            # NE
            elif self._world_padded[row, col-1] == 0 and self._world_padded[row, col+1] == 1 and self._world_padded[row-1, col] == 1 and self._world_padded[row+1, col] == 0:
                return self._roadNE
            # NW
            elif self._world_padded[row, col-1] == 1 and self._world_padded[row, col+1] == 0 and self._world_padded[row-1, col] == 1 and self._world_padded[row+1, col] == 0:
                return self._roadNW
            # SE
            elif self._world_padded[row, col-1] == 0 and self._world_padded[row, col+1] == 1 and self._world_padded[row-1, col] == 0 and self._world_padded[row+1, col] == 1:
                return self._roadSE
            # SW
            elif self._world_padded[row, col-1] == 1 and self._world_padded[row, col+1] == 0 and self._world_padded[row-1, col] == 0 and self._world_padded[row+1, col] == 1:
                return self._roadSW
            # WNS
            elif self._world_padded[row, col-1] == 1 and self._world_padded[row, col+1] == 0 and self._world_padded[row-1, col] == 1 and self._world_padded[row+1, col] == 1:
                return self._roadWNS
            # NES
            elif self._world_padded[row, col-1] == 0 and self._world_padded[row, col+1] == 1 and self._world_padded[row-1, col] == 1 and self._world_padded[row+1, col] == 1:
                return self._roadNES
            # WES
            elif self._world_padded[row, col-1] == 1 and self._world_padded[row, col+1] == 1 and self._world_padded[row-1, col] == 0 and self._world_padded[row+1, col] == 1:
                return self._roadWES
            # WNE
            elif self._world_padded[row, col-1] == 1 and self._world_padded[row, col+1] == 1 and self._world_padded[row-1, col] == 1 and self._world_padded[row+1, col] == 0:
                return self._roadWNE
            # END
            elif self._world_padded[row, col-1] == 0 and self._world_padded[row, col+1] == 0 and self._world_padded[row-1, col] == 0 and self._world_padded[row+1, col] == 0:
                return self._roadEND
            else:
                return self._roadEND
            
        else:
            raise ValueError(f"Invalid map tile id `{self._world_padded[row, col]}`.")

    def render(self, screen):

        for index, tile_id in np.ndenumerate(self._world): 
            row, col = index
            tile = self._get_tile(row, col)
            position = (col * self._TILE_SIZE + self._x_offset, row * self._TILE_SIZE + self._y_offset)
            screen.blit(tile, position)

    def update(self, offset):

        self._x_offset, self._y_offset = offset
