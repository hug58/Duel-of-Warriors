from math import radians

import pygame as pg
import pymunk
import math

from components.items import Item
from components.player import Player
from pymunk.vec2d import Vec2d

class Arrow(Item):
    def __init__(self, x:int,y:int, angle: int, time_charge:int, player:Player, screen: pg.Surface):
        route = "assets/arrow.png"
        Item.__init__(self, route, screen,0, player)

        self.angle = angle
        self.x = x
        self.y = y

        size = self.image.get_size()
        self.time_charge = time_charge if time_charge < 1000 else 1000
        self.body = pymunk.Body(2,  pymunk.moment_for_box(1, size ))

        self.body.position = x, y
        self.body.angle = math.radians(angle)
        self.shape = pymunk.Poly.create_box(self.body, self.image.get_size())
        self.shape.elasticity = 0.5
        self.shape.collision_type = 3
        self.shape.color = (255, 0, 0, 255)  # red


    def update(self):
        self.x, self.y = self.body.position
        self.angle = self.body.angle
        self.rect.center = (self.x,self.y)


    def actions(self):
        # Define the magnitude of the force
        force_magnitude = 2000 + self.time_charge
        _radians = math.radians(self.angle) * -1
        impulse = Vec2d.from_polar(force_magnitude, _radians)
        self.body.apply_impulse_at_world_point(impulse, self.body.position)


    def draw(self):
        surface = self.image
        angle = math.degrees(self.angle) % 360

        if angle != 0:
            surface = pg.transform.rotate(surface,angle)

        new_rect = surface.get_rect(center=self.rect.center)
        self.screen.blit(surface,  new_rect.topleft)


    def __str__(self):
        return f"ARROW: {self.time_charge}"


class Arc(Item):

    def __init__(self,count:int, screen: pg.Surface, player: Player):
        route = "assets/arc.png"
        self.player = player
        self.time__max_change = 200  #milliseconds
        Item.__init__(self, route, screen, count, self.player)


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
        arrow:Arrow = Arrow(self.rect.centerx,self.rect.centery, self.angle, 
                            self.time_charge,self.player, self.screen)
        arrow.actions()

        return self.get_counter(), arrow


    def __str__(self):
        return "ARC"
    


class Shield(Item):

    def __init__(self,count:int, screen: pg.Surface, player: Player):
        route = "assets/shield.png"
        self.player = player
        self.time__max_change = 200  #milliseconds
        Item.__init__(self, route, screen, count, self.player)
        self.image = pg.transform.scale(self.image,(16,32))
        self._visible = False


    def update(self):
        self.angle = self.player.angle_arc

        for item_group in self.player.items_group:
            item_group: Item
            if pg.Rect.colliderect(self.rect, item_group.rect):
                if self._visible:
                    self.player.items_group.remove(item_group)
                    self.player.space.remove(item_group.body, item_group.shape)



        super().update()



    def can_show(self):
        angle_rad = math.radians(self.player.angle_arc)  # Convert angle to radians
        distance = 20  # Distance from the player to the arc
        self.rect.x = self.player.rect.x + distance * math.cos(angle_rad)
        self.rect.y = self.player.rect.y - distance * math.sin(angle_rad)

        # self.body.position = self.rect.x, self.rect.y
        # self.body.apply_force_at_world_point((0, -self.player.space.gravity[1] * self.body.mass), self.body.position)
        # self.body.angle = angle_rad * -1





    def __str__(self):
        return "SHIELD"