"""
:CLASS PLAYER:
"""

from typing import List, Optional
import math
import pygame as pg
import pymunk
from components.items import Item
from collections import OrderedDict

SIZE_PLAYER = (16,16)

class Player:

    VLY = 19
    GRAVITY = 3.2

    def __init__(self, pos_x:int,pos_y:int, space, items_group: pg.sprite.Group):
        self.rect = pg.rect.Rect(pos_x, pos_y, SIZE_PLAYER[0], SIZE_PLAYER[1])

        self.body:pymunk.Body = pymunk.Body(5, 5, body_type=pymunk.Body.DYNAMIC)
        self.body.position = pos_x, pos_y
        self.body.moment =  float("inf")
        self.body.angle = 0
        self.shape = pymunk.Poly.create_box(self.body, SIZE_PLAYER)
        self.shape.collision_type = 2 #identity collision
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
        self.list_inventory:List[tuple] = list(self.inventory.items())
        self.index_select_inventory:int = 0

        self._angle = 0
        self._angle_arc = 0
        self.x = pos_x
        self.y = pos_y

        self.space: pymunk.Space = space
        self.items_group:pg.sprite.Group = items_group


    def load(self):
        pg.draw.rect(self.surface, self.color, (0,0, self.rect.width, self.rect.height))


    def update(self):
        self.x, self.y = self.body.position
        self._angle = self.body.angle

        for i,_item in self.list_inventory:
            _item:Item
            _item.update()


    def move(self, direction: int):
        max_speed = 250

        speed = self.body.velocity.length
        if speed > max_speed:
            self.body.velocity = self.body.velocity.normalized() * max_speed

        if direction == 1:
            force = (3000, 0)  # Fuerza hacia la derecha
            self.body.apply_force_at_local_point(force, (0, 0))
        elif direction == -1:
            force = (-3000, 0)  # Fuerza hacia la derecha
            self.body.apply_force_at_local_point(force, (0, 0))


    def jump(self):
        force = (0, -2500)
        self.body.apply_impulse_at_local_point(force)
        # self.jump_on = False
        self.move_on = False


    def actions(self,time_charge=0):
        key_item, item = self.list_inventory[self.index_select_inventory]
        if key_item == "arc": 
            key,arrow = item.actions()
            item.time_charge = time_charge


            if key > 0:
                self.space.add(arrow.body, arrow.shape)
            else:
                item.time_init_reload = pg.time.get_ticks()
                item.reload_action = True
                
            self.items_group.add(arrow)


    def draw(self, screen: pg.Surface):
        self.rect.center = (self.x,self.y)
        screen.blit(self.surface, self.rect)

        for key,item in self.list_inventory:
            item: Item
            if item.visible:
                item.draw()


    def add_item_to_inventory_without_space(self, key: str, item: Item):
        self.inventory[key] = item
        self.list_inventory =  list(self.inventory.items())


    def add_item_to_inventory(self,key:str, item: Item):
        self.inventory[key] = item
        self.space.add(item.body, item.shape)
        self.list_inventory =  list(self.inventory.items())


    def select_inventory(self, direction):

        if len(self.list_inventory) > 0:
            item: Item = self.list_inventory[self.index_select_inventory][1]
            item.visible = False

            try:
                self.index_select_inventory += direction
                item: Item = self.list_inventory[self.index_select_inventory][1]
            except IndexError:
                if direction > 0:
                    self.index_select_inventory = 0
                else:
                    self.index_select_inventory = len(self.list_inventory) -1

                item: Item = self.list_inventory[self.index_select_inventory][1]


            item.visible = True
            return self.index_select_inventory
                
        return None



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