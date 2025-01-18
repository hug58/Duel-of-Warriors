from math import radians

import pygame as pg
import pymunk
import math

from components.items import Item
from components.player import Player
from pymunk.vec2d import Vec2d

class Arrow(Item):
    def __init__(self, x:int,y:int, angle: int, screen: pg.Surface):
        route = "assets/arrow.png"
        Item.__init__(self, route, screen,0)

        self.angle = angle
        self.x = x
        self.y = y

        size = self.image.get_size()

        self.body = pymunk.Body(1,  pymunk.moment_for_box(1, size ))
        # self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)

        self.body.position = x, y
        self.body.angle = math.radians(angle)
        self.shape = pymunk.Poly.create_box(self.body, self.image.get_size())
        self.shape.elasticity = 0.5


    def update(self):
        self.x, self.y = self.body.position
        self.angle = self.body.angle
        self.rect.center = (self.x,self.y)



    def actions(self):
        # Define the magnitude of the force
        force_magnitude = 600

        _radians = math.radians(self.angle) * -1
        impulse = Vec2d.from_polar(force_magnitude, _radians)
        self.body.apply_impulse_at_world_point(impulse, self.body.position)


    def draw(self):
        surface = self.image
        angle = math.degrees(self.angle) % 360

        surface = pg.transform.rotate(surface,angle)
        new_rect = surface.get_rect(center=self.rect.center)
        self.screen.blit(surface,  new_rect.topleft)


    def __str__(self):
        return "ARROW"


class Arc(Item):
    def __init__(self, screen: pg.Surface, player: Player):
        route = "assets/arc.png"
        self.player = player
        Item.__init__(self, route, screen,10)


    def update(self):
        self.angle = self.player.angle_arc
        super().update()


    def can_show(self):
        angle_rad = math.radians(self.angle)  # Convert angle to radians
        distance = 30  # Distance from the player to the arc
        self.rect.x = self.player.rect.x + distance * math.cos(angle_rad)
        self.rect.y = self.player.rect.y - distance * math.sin(angle_rad)


    def actions(self):
        """

        :return:
        """

        get_counter = self.get_counter()
        if get_counter:
            arrow:Arrow = Arrow(self.rect.centerx,self.rect.centery, self.angle, self.screen)
            arrow.actions()

            return self.get_counter(), arrow

        return -1, None


    def __str__(self):
        return "ARC"