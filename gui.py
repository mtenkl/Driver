import pygame
import pygame.freetype


class ShifterGui(pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()

        self.font = pygame.freetype.SysFont(
            pygame.freetype.get_default_font(), 20)

        self.width = 20
        self.height = 60
        self.size = 5
        self.image = pygame.Surface((self.width, self.height))
        self.NOT_SELECTED_COLOR = (0, 200, 200)
        self.SELECTED_COLOR = (255, 0, 0)

    def update(self, drive_mode: str, selected_gear: int):

        self.image = pygame.Surface((30, 140))
        
        #self.image.set_alpha(100)

        p, _ = self.font.render("P", self.SELECTED_COLOR if drive_mode == "P" else self.NOT_SELECTED_COLOR)
        r, _ = self.font.render("R", self.SELECTED_COLOR if drive_mode == "R" else self.NOT_SELECTED_COLOR)
        n, _ = self.font.render("N", self.SELECTED_COLOR if drive_mode == "N" else self.NOT_SELECTED_COLOR)
        d, _ = self.font.render("D", self.SELECTED_COLOR if drive_mode == "D" else self.NOT_SELECTED_COLOR)
        gear, _ = self.font.render(str(selected_gear), (0,200,0))
        

        self.image.blit(p, (10, 10))
        self.image.blit(r, (10, 30))
        self.image.blit(n, (10, 50))
        self.image.blit(d, (10, 70))
        self.image.blit(gear, (10, 120))
