import pygame
import pygame.freetype


class BidirectionalProgressBar():

    def __init__(self, surface, rect: pygame.Rect, range_min, range_max, color=(255, 255, 255)) -> None:

        self._surface = surface
        self._frame_rect = rect
        self._range_min = range_min
        self._range_max = range_max
        self._scale = self._frame_rect.width / \
            (self._range_max - self._range_min)

        self._color = color

    def set_value(self, value):

        if value > 0:
            progress_bar = pygame.Rect(
                self._frame_rect.centerx, self._frame_rect.top, value * self._scale, self._frame_rect.height)
        else:
            progress_bar = pygame.Rect(self._frame_rect.centerx + value * self._scale,
                                       self._frame_rect.top, -value * self._scale, self._frame_rect.height)

        # Frame
        pygame.draw.rect(self._surface, self._color, self._frame_rect, 2)
        # Progress bar
        pygame.draw.rect(self._surface, self._color, progress_bar)


class MiniMap(pygame.sprite.Sprite):

    def __init__(self, shape: tuple[int, int], scale:float) -> None:
        super().__init__()
        self._shape = shape
        self._scale = scale

        self.image = pygame.Surface(self._shape)
        self.rect = self.image.get_rect()

    def update(self, vehicle_pos):

        self.image = pygame.Surface(tuple(x * self._scale for x in self._shape))
        self.rect = self.image.get_rect()

        pygame.draw.circle(self.image, (0, 255, 255), tuple(x*self._scale for x in vehicle_pos), 2)

