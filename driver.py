import pygame
import math
from pygame import Rect, Vector2
import pygame.freetype
import pygame_gui
from vehicle import vehicledynamics
import gui
import numpy as np
import mapgenerator
from pid import PID
from trajectory import Trajectory
from trajectory import Node


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


def main():

    pygame.init()
    pygame.display.set_caption("Driver")

    clock = pygame.time.Clock()
    WIDTH = 840
    HEIGHT = 680
    SCALE = 30

    manager = pygame_gui.UIManager((WIDTH, HEIGHT))
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    background = mapgenerator.MapGenerator("world-map.csv")
    background.render(screen)
    player = Car((WIDTH/2, HEIGHT/2))
    trajectory = Trajectory(300, 0.1)
    mini_map = gui.MiniMap(tuple(x/SCALE for x in background.shape[::-1]), 0.5)

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

        player.update(pressed_keys, dt)
        trajectory.add(
            Node(player.vehicle.x, player.vehicle.y, player.vehicle.theta))
        background.set_offset(
            (-player.vehicle.x * SCALE, -player.vehicle.y * SCALE))
        mini_map.update((player.vehicle.x, player.vehicle.y))
        background.render(screen)

        vehicle_speed_label.set_text(
            f"Speed: {str(round(player.vehicle.vehicle_speed_kmph)).rjust(3)} km/h")
        vehicle_acc_label.set_text(
            f"Acceleration: {str(round(player.vehicle.acceleration_mps2)).rjust(3)} m/s2")
        vehicle_pos_label.set_text(
            f"Position: [{round(player.vehicle.x)}, {round(player.vehicle.y)}] m")
        vehicle_steering_progress_bar.set_value(player.wheel_angle_deg)

        trajectory.draw(screen, SCALE, -player.vehicle.x * SCALE + WIDTH/2, SCALE, -player.vehicle.y * SCALE + HEIGHT/2)
        screen.blit(mini_map.image, mini_map.rect)
        screen.blit(player.image, player.rect)

        pygame.draw.circle(screen, (0, 100, 255), player.rect.center, 3)
        pygame.draw.circle(screen, (0, 255, 255), player.axis_center, 1)

        manager.draw_ui(screen)
        pygame.display.update()


if __name__ == "__main__":
    main()
