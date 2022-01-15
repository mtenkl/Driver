import unittest
import driver
import pygame

class TestBackground(unittest.TestCase):


    def test_init(self):

        bkg = driver.Background()
        pass

    def test_render(self):

        pygame.init()
        pygame.display.set_caption("Test Driver")
        WIDTH = 800
        HEIGHT = 800

        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        bkg = driver.Background()
        running = True
        while running:

            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                    running = False

            bkg.render(screen)

            pygame.display.update()
