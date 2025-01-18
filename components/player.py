"""
:CLASS PLAYER:
"""

from typing import List
import math
import pygame as pg
import pymunk
from components.items import Item

SIZE_PLAYER = (16,16)

class Player:

    VLY = 19
    GRAVITY = 3.2

    def __init__(self, pos_x:int,pos_y:int, space):
        self.rect = pg.rect.Rect(pos_x, pos_y, SIZE_PLAYER[0], SIZE_PLAYER[1])

        self.body = pymunk.Body(1, 5, body_type=pymunk.Body.DYNAMIC)
        self.body.position = pos_x, pos_y
        self.body.angle = 0
        self.shape = pymunk.Poly.create_box(self.body, SIZE_PLAYER)
        self.shape.collision_type = 2
        self.shape.elasticity = 0.5

        self.surface = pg.Surface(self.rect.size)
        self.color = (20,82,80)
        self.vly = 3
        self.vlx = 3

        self.load()
        self.mask = pg.mask.from_surface(self.surface)
        self.jump_on = True
        self.move_on = False

        self.inventory:dict = {}
        self._angle = 0
        self._angle_arc = 0
        self.x = pos_x
        self.y = pos_y

        self.space: pymunk.Space = space


    def load(self):
        pg.draw.rect(self.surface, self.color, (0,0, self.rect.width, self.rect.height))


    def update(self):
        self.x, self.y = self.body.position
        self._angle = self.body.angle

        for i,_item in self.inventory.items():
            _item:Item
            _item.update()


    def move(self, direction: int):
        max_speed = 250

        speed = self.body.velocity.length
        if speed > max_speed:
            self.body.velocity = self.body.velocity.normalized() * max_speed

        if direction == 1:
            force = (1000, 0)  # Fuerza hacia la derecha
            self.body.apply_force_at_local_point(force, (0, 0))
        elif direction == -1:
            force = (-1000, 0)  # Fuerza hacia la derecha
            self.body.apply_force_at_local_point(force, (0, 0))


    def jump(self):
        force = (0, -200)
        self.body.apply_impulse_at_local_point(force, (0, 0))
        self.jump_on = False
        self.move_on = False


    def actions(self, key_item:str):
        item: Item = self.inventory[key_item]
        key,arrow = item.actions()

        if key > -1:
            self.inventory[f"ARROW_{key}"] = arrow
            self.space.add(arrow.body, arrow.shape)


    def draw(self, screen: pg.Surface):
        self.rect.center = (self.x,self.y)
        screen.blit(self.surface, self.rect)

        for key,item in self.inventory.items():
            item: Item
            item.draw()

    def add_item_to_inventory_without_space(self, key: str, item: Item):
        self.inventory[key] = item

    def add_item_to_inventory(self,key:str, item: Item):
        self.inventory[key] = item
        self.space.add(item.body, item.shape)


    @property
    def angle_arc(self):
        return self._angle_arc


    @angle_arc.setter
    def angle_arc(self, pos_b):
        if pos_b[0] == self.body.position.x:
            self._angle_arc = 90
        else:
            pos_a = self.body.position

            delta_x = pos_b[0] - pos_a[0]
            delta_y = pos_a[1] - pos_b[1]

            radians = math.atan2(delta_y, delta_x)
            self._angle_arc = math.degrees(radians)
            self._angle_arc = self._angle_arc % 360