import imp
from lib2to3.pgen2.driver import Driver
import pygame
import math
from pygame import Rect, Vector2
import pygame.freetype
from pygame.sndarray import array
import pygame_gui
import vehicle as vm
from vehicle import vehicledynamics
import gui
import numpy as np
import mapgenerator
from pid import PID


class Car(pygame.sprite.Sprite):

    def __init__(self, position: tuple, scale=30) -> None:
        super().__init__()
        self.SCALE = scale

        self.vehicle = vehicledynamics.VehicleDynamicModel3dof("mazda.ini")
        self.vehicle.ignition_on = True
        self.vehicle.drive_mode = "P"
        self.vehicle.set_position(x=0, y=0, theta=0)

        self.ORIGINAL_IMAGE = pygame.image.load("porsche.bmp").convert_alpha()
        self.image = self.ORIGINAL_IMAGE
        self.rect = self.ORIGINAL_IMAGE.get_rect()
        self.rect.centerx, self.rect.centery = position

        self.orientation_deg = math.degrees(-self.vehicle.theta)
        self.wheel_angle_deg = math.degrees(self.vehicle.wheel_angle)
        self.VEHICLE_CENTER_OFFSET = Vector2(1.3, 0)

        self.pid = PID(10, 10, 0, math.radians(-100), math.radians(100))

    def update(self, pressed_keys, dt):

        if pressed_keys[pygame.K_UP]:
            self.vehicle.throttle_pedal = 80
            self.vehicle.brake_pedal = 0
        elif pressed_keys[pygame.K_DOWN]:
            self.vehicle.throttle_pedal = 0
            self.vehicle.brake_pedal = 90
        else:
            self.vehicle.throttle_pedal = 0
            self.vehicle.brake_pedal = 0

        if pressed_keys[pygame.K_LEFT]:
            steering_speed = math.radians(-80)
        elif pressed_keys[pygame.K_RIGHT]:
            steering_speed = math.radians(80)
        else:
            steering_speed = self.pid.output(self.vehicle.wheel_angle, 0, dt)

        if pressed_keys[pygame.K_p]:
            self.vehicle.drive_mode = "P"
        elif pressed_keys[pygame.K_r]:
            self.vehicle.drive_mode = "R"
        elif pressed_keys[pygame.K_n]:
            self.vehicle.drive_mode = "N"
        elif pressed_keys[pygame.K_d]:
            self.vehicle.drive_mode = "D"

        self.vehicle.update(dt)
        x, y, theta = self.vehicle.steering(
            self.vehicle.vehicle_speed_mps, steering_speed, dt)
        theta_deg = math.degrees(-theta)
        self.wheel_angle_deg = math.degrees(self.vehicle.wheel_angle)

        rotated_offset = self.VEHICLE_CENTER_OFFSET.rotate(-theta_deg)

        self.image = pygame.transform.rotate(self.ORIGINAL_IMAGE, theta_deg)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.axis_center = self.rect.center - rotated_offset


class WheelGui(pygame.sprite.Sprite):

    def __init__(self, position, steering=False) -> None:
        super().__init__()

        self.steering = steering
        self.surf = pygame.Surface([10, 20], pygame.SRCALPHA)
        pygame.draw.rect(self.surf, (255, 0, 0), pygame.Rect(0, 0, 10, 20), 1)
        self.image = self.surf
        self.rect = self.surf.get_rect()
        self.rect.center = position

    def update(self, angle):
        if self.steering:
            self.rotated = pygame.transform.rotate(self.surf, -angle)
            self.rect = self.rotated.get_rect(center=(self.rect.center))
            self.image = self.rotated


class CarGui(pygame.sprite.Group):

    def __init__(self) -> None:
        super().__init__()

        self.add(WheelGui((50, 50), steering=True))
        self.add(WheelGui((100, 50), steering=True))
        self.add(WheelGui((50, 170), steering=False))
        self.add(WheelGui((100, 170), steering=False))

    def update(self, slip_angle):
        for sprite in self.sprites():
            sprite.update(slip_angle)


class TrajectoryPoint(pygame.sprite.Sprite):

    def __init__(self, point) -> None:
        super().__init__()

        self.image = pygame.Surface([2, 2], pygame.SRCALPHA)
        self.image.fill((0, 200, 0))

        self.rect = self.image.get_rect()
        self.rect.center = (point[0], point[1])


def main():

    pygame.init()
    pygame.display.set_caption("Driver")

    font = pygame.freetype.SysFont(pygame.freetype.get_default_font(), 14)
    clock = pygame.time.Clock()
    WIDTH = 840
    HEIGHT = 680
    SCALE = 30

    manager = pygame_gui.UIManager((WIDTH, HEIGHT))

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    background = mapgenerator.MapGenerator("world-map.csv")
    background.render(screen)

    player = Car((WIDTH/2, HEIGHT/2))
    hud = CarGui()
    traj = pygame.sprite.Group()

    drive_program_selector = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect(
        (10, HEIGHT - 100), (30, 86)), item_list=["P", "R", "N", "D"], manager=manager)
    vehicle_speed_label = pygame_gui.elements.ui_label.UILabel(relative_rect=pygame.Rect(
        (WIDTH - 200, HEIGHT - 40), (180, 30)), text="", manager=manager)
    vehicle_pos_label = pygame_gui.elements.ui_label.UILabel(relative_rect=pygame.Rect(
        (WIDTH - 200, HEIGHT - 70), (180, 30)), text="", manager=manager)
    vehicle_acc_label = pygame_gui.elements.ui_label.UILabel(relative_rect=pygame.Rect(
        (WIDTH - 200, HEIGHT - 100), (180, 30)), text="", manager=manager)
    vehicle_steering_progress_bar = gui.BidirectionalProgressBar(screen, pygame.Rect(
        (WIDTH - 200, HEIGHT - 130), (180, 30)), -player.vehicle.STEERING_TIRE_ANGLE_MAX, player.vehicle.STEERING_TIRE_ANGLE_MAX)

    running = True

    while running:

        dt = clock.tick(30) / 1000

        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

            if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
                if event.ui_element == drive_program_selector:
                    player.vehicle.drive_mode = event.text

            manager.process_events(event)

        pressed_keys = pygame.key.get_pressed()
        manager.update(dt)

        screen.fill((255, 255, 255))
        background.render(screen)

        player.update(pressed_keys, dt)
        background.update(
            (-player.vehicle.x * SCALE, -player.vehicle.y * SCALE))
        hud.update(player.wheel_angle_deg)
        traj.add(TrajectoryPoint((player.vehicle.x, player.vehicle.y)))
        traj.update()

        vehicle_speed_label.set_text(
            f"Speed: {str(round(player.vehicle.vehicle_speed_kmph)).rjust(3)} km/h")
        vehicle_acc_label.set_text(
            f"Acceleration: {str(round(player.vehicle.acceleration_mps2)).rjust(3)} m/s2")
        vehicle_pos_label.set_text(
            f"Position: [{round(player.vehicle.x)}, {round(player.vehicle.y)}] m")
        vehicle_steering_progress_bar.set_value(player.wheel_angle_deg)

        traj.draw(screen)
        hud.draw(screen)

        screen.blit(player.image, player.rect)
        pygame.draw.circle(screen, (0, 100, 255), player.rect.center, 2)
        pygame.draw.circle(screen, (0, 255, 255), player.axis_center, 2)

        manager.draw_ui(screen)

        pygame.display.update()


if __name__ == "__main__":
    main()
