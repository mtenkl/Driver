import unittest
import mapgenerator
import pygame
import numpy as np


class TestMapGenerator(unittest.TestCase):

    def test_loading_map(self):
        mg = mapgenerator.MapGenerator("tests/world-map-test.csv")
        shape = mg._world.shape
        self.assertEqual(shape, (8,17))
        

    def test_get_tile(self):
        
        mg = mapgenerator.MapGenerator("tests/world-map-test.csv")

        mg._world_padded = np.array([[0,0,0],
                                     [0,0,0],
                                     [0,0,0]])
        texture = mg._get_tile(0, 0)
        self.assertIs(texture, mg._roadPLAZA, "Plaza")

        mg._world_padded = np.array([[0,0,0],
                                     [0,1,0],
                                     [0,0,0]])
        texture = mg._get_tile(0, 0)
        self.assertIs(texture, mg._roadNEWS, "NEWS")

        mg._world_padded = np.array([[0,1,0],
                                     [1,1,1],
                                     [0,1,0]])
        texture = mg._get_tile(0, 0)
        self.assertIs(texture, mg._roadNEWS, "NEWS")

        mg._world_padded = np.array([[0,0,0],
                                     [1,1,1],
                                     [0,0,0]])
        texture = mg._get_tile(0, 0)
        self.assertIs(texture, mg._roadEW, "EW")

        mg._world_padded = np.array([[0,1,0],
                                     [0,1,0],
                                     [0,1,0]])
        texture = mg._get_tile(0, 0)
        self.assertIs(texture, mg._roadNS, "NS")

        mg._world_padded = np.array([[0,1,0],
                                     [0,1,1],
                                     [0,0,0]])
        texture = mg._get_tile(0, 0)
        self.assertIs(texture, mg._roadNE, "NE")

        mg._world_padded = np.array([[0,1,0],
                                     [1,1,0],
                                     [0,0,0]])
        texture = mg._get_tile(0, 0)
        self.assertIs(texture, mg._roadNW, "NW")

        mg._world_padded = np.array([[0,0,0],
                                     [1,1,0],
                                     [0,1,0]])
        texture = mg._get_tile(0, 0)
        self.assertIs(texture, mg._roadSW, "SW")

        mg._world_padded = np.array([[0,0,0],
                                     [0,1,1],
                                     [0,1,0]])
        texture = mg._get_tile(0, 0)
        self.assertIs(texture, mg._roadSE, "SE")

        mg._world_padded = np.array([[0,1,0],
                                     [0,1,1],
                                     [0,1,0]])
        texture = mg._get_tile(0, 0)
        self.assertIs(texture, mg._roadNEWS, "ALL")


    def test_display_map(self):
        WIDTH = 1024
        HEIGHT = 680
    
        pygame.init()
        pygame.display.set_caption("Map")
        screen = pygame.display.set_mode((WIDTH, HEIGHT))

        mg = mapgenerator.MapGenerator("tests/world-map-test.csv")
        offset = pygame.Vector2(0,0)

        running = True
        while running:

            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                    running = False

            pressed_keys = pygame.key.get_pressed()

            if pressed_keys[pygame.K_UP]:
                offset = offset + pygame.Vector2(0,10)
            if pressed_keys[pygame.K_DOWN]:
                offset = offset + pygame.Vector2(0,-10)
            if pressed_keys[pygame.K_LEFT]:
                offset = offset + pygame.Vector2(10,0)
            if pressed_keys[pygame.K_RIGHT]:  
                offset = offset + pygame.Vector2(-10,0)
                
            mg.update(offset)
            mg.render(screen)
            pygame.display.update()


