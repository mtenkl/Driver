import pygame
import math
from pygame import Vector2



class Car(pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
        self.surf = pygame.image.load("porsche.bmp").convert_alpha()
        self.rect = self.surf.get_rect()
        self.rect.center = (10, 100)

        self.position = Vector2(10, 10)
        self.orientation_deg = 0
        self.velocity_ms = Vector2(0, 0)

        self.acceleration_mss = 0

        self.MAX_ACCELERATION_MSS = 5
        self.BRAKING_ACCELERATION_MSS = -9
        self.ENGINE_BRAKING_ACCELERATION_MSS = -3
        self.HANDBRAKE_ACCELERATION_MSS = -4

        self.wheel_angle_deg = 0
        self.MAX_WHEEL_ANGLE_DEG = 60

        self.VEHICLE_LENGTH_M = 4.5
        
       

    def update(self, pressed_keys, dt):

        if pressed_keys[pygame.K_UP]:
            if self.velocity_ms.x >= 0:
                self.acceleration_mss = self.MAX_ACCELERATION_MSS
            else:
                self.acceleration_mss = -self.BRAKING_ACCELERATION_MSS

        elif pressed_keys[pygame.K_DOWN]:
            if self.velocity_ms.x > 0:
                self.acceleration_mss = self.BRAKING_ACCELERATION_MSS
            else:
                self.acceleration_mss = -self.MAX_ACCELERATION_MSS

        elif pressed_keys[pygame.K_SPACE]:
            self.acceleration_mss = -math.copysign(self.HANDBRAKE_ACCELERATION_MSS, self.velocity_ms.x)
        else:
            self.acceleration_mss = -math.copysign(self.ENGINE_BRAKING_ACCELERATION_MSS, self.velocity_ms.x)
            if self.velocity_ms.x > 0.01:
                self.acceleration_mss = self.ENGINE_BRAKING_ACCELERATION_MSS
            elif self.velocity_ms.x < -0.01:
                self.acceleration_mss = - self.ENGINE_BRAKING_ACCELERATION_MSS
            else:
                self.acceleration_mss = 0
                self.velocity_ms.x = 0

        if pressed_keys[pygame.K_LEFT]:
            self.wheel_angle_deg += 120 * dt
        elif pressed_keys[pygame.K_RIGHT]:  
            self.wheel_angle_deg -= 120 * dt
        else:
            if self.wheel_angle_deg > 0:
                self.wheel_angle_deg = max(0, self.wheel_angle_deg - 120 * dt)
            else:
                self.wheel_angle_deg = min(0, self.wheel_angle_deg + 120 * dt)


        self.wheel_angle_deg = max(-self.MAX_WHEEL_ANGLE_DEG, min(self.wheel_angle_deg, self.MAX_WHEEL_ANGLE_DEG))


        if self.wheel_angle_deg != 0:
            turning_radius = self.VEHICLE_LENGTH_M / math.sin(math.radians(self.wheel_angle_deg))
            angular_velocity = self.velocity_ms.x / turning_radius
        else:
            angular_velocity = 0

        self.velocity_ms += (self.acceleration_mss * dt, 0)


        self.position += self.velocity_ms.rotate(-self.orientation_deg) * dt

        self.orientation_deg += math.degrees(angular_velocity) * dt

        self.rotated = pygame.transform.rotate(self.surf, self.orientation_deg)
        self.rect = self.rotated.get_rect()
        


class CarHUD(pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()

        self.surf = pygame.Surface([20, 30], pygame.SRCALPHA)
        self.surf.fill((255,0,0))

        self.rect = self.surf.get_rect()
        self.rect.center = (30, 30)

    def update(self, angle):
        self.rotated = pygame.transform.rotate(self.surf, angle)
        self.rect = self.rotated.get_rect(center=(30,30))

class TrajectoryPoint(pygame.sprite.Sprite):

        def __init__(self, point) -> None:
            super().__init__()

            self.image = pygame.Surface([2, 2], pygame.SRCALPHA)
            self.image.fill((0,200,0))

            self.rect = self.image.get_rect()
            self.rect.center = (point[0] * 30, point[1] * 30)

     



def main():

    pygame.init()
    pygame.display.set_caption("Driver")

    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((840, 680))

    running = True


    player = Car()
    hud = CarHUD()

    traj = pygame.sprite.Group()

    while running:

        dt = clock.tick(30) / 1000

        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

        pressed_keys = pygame.key.get_pressed()
        
        screen.fill((255, 255, 255))

        player.update(pressed_keys, dt)
        hud.update(player.wheel_angle_deg)
        traj.add(TrajectoryPoint(player.position))
        traj.update()

        print("Speed: {} m/s Acc: {}, Wheel: {}, Orientation: {}".format(player.velocity_ms, player.acceleration_mss, player.wheel_angle_deg, player.orientation_deg))

        traj.draw(screen)
        screen.blit(player.rotated, player.position * 30 - (player.rect.width /2, player.rect.height /2))
        screen.blit(hud.rotated, hud.rect)
        
        pygame.display.update()
        


if __name__ == "__main__":
    main()