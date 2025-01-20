#!/usr/bin/python3
""" this is the manager game """

import pygame as pg
import pymunk
import pymunk.pygame_util

from typing import Dict
from components.player import Player
from components.weapons import Arc, Shield, Item



players:Dict[int, Player] = {}

def create_floor(size: tuple,x:int,y:int,space: pymunk.Space):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (x, y)
    
    shape = pymunk.Poly.create_box(body, size)
    shape.friction = 1
    shape.collision_type = 1

    space.add(body, shape)




def collision_handler(arbiter, space: pymunk.Space, data):
    shape_a = arbiter.shapes[0]
    shape_b = arbiter.shapes[1].collision_type
    player:Player = players[shape_b]
    player.jump_on = True
    player.move_on = True
    # player.body.velocity = (0,0)

    return True


def collision_handler_arrow(arbiter, space: pymunk.Space, data):
    shape_a = arbiter.shapes[0]
    shape_b: pymunk.Shape = arbiter.shapes[1]
    body: pymunk.Body = shape_b.body
    body.velocity = (0,0)

    # space.remove(shape_b, body)

    return True


class Game:
    def __init__(self,screen:pg.Surface):
        self.screen = screen
        self.image =  pg.Surface(screen.get_size())

        self.space = pymunk.Space()
        self.space.gravity = (0, 980)
        self.items_group = pg.sprite.Group()

        self.player = Player(100,100, self.space, self.items_group)
        self.player.add_item_to_inventory_without_space("shield",Shield(100,self.image, self.player))
        self.player.add_item_to_inventory_without_space("arc",Arc(100,self.image, self.player))
        self.player.select_inventory(1)


        self.space.add(self.player.body, self.player.shape)
        height = screen.get_size()[1]
        width = screen.get_size()[0]
        
        create_floor(size=(width,20),x=width//2,y=height +5, space= self.space)
        create_floor(size=(5,height),x=5,y=height//2, space= self.space)
        create_floor(size=(5,height),x=width - 5,y=height//2, space= self.space)

        #platform
        create_floor(size=(100,20),x=300,y=300, space= self.space)
        create_floor(size=(100,20),x=500,y=200, space= self.space)


        # Set up collision handler
        players[2] = self.player
        handler = self.space.add_collision_handler(1, 2)  # Assuming 1 for floor and 2 for player
        handler.begin = collision_handler

        handler2 = self.space.add_collision_handler(1, 3)
        handler2.begin = collision_handler_arrow

        self.count_inventory = len(self.player.inventory)
        self.draw_options = pymunk.pygame_util.DrawOptions(self.image)


        self.zoom_level = 1.0
        self.zoom_factor = 0.2
        self.max_zoom = 2.0
        self.min_zoom = 1.0


        self.time_charge_start = 0
        self.time_charge_end = 0




    def update(self):
        """ Update Game"""

        self.player.update()

        for item in self.items_group:
            item: Item
            item.update()

        self.space.step(1 / 60.0)


    def draw(self):
        """ Draw the player and scene. """
        self.image.fill((0,0,0))
        self.player.draw(self.image)

        for item in self.items_group:
            item: Item
            item.draw()

        # Draw the floor

        self.space.debug_draw(self.draw_options)
        self.scale = pg.transform.scale(self.image, (self.image.get_width() * self.zoom_level, self.image.get_height() * self.zoom_level))

        # Calcular el desplazamiento basado en la posición del jugador
        offset_x = self.player.rect.x - (self.screen.get_width() // 2)
        offset_y = self.player.rect.y + (self.screen.get_height() // 2)  # Ajuste para la coordenada Y invertida

        # Dibujar la imagen escalada en la pantalla con los desplazamientos calculados
        self.screen.blit(self.scale, (-offset_x * (self.zoom_level - 1), -offset_y * (self.zoom_level - 1)))


    def __str__(self):
        return "Game Test"