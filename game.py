#!/usr/bin/python3
""" this is the manager game """

import pygame as pg
import pymunk
import pymunk.pygame_util

from typing import Dict
from components.player import Player
from components.weapons import Arc



players:Dict[int, Player] = {}

def create_floor(pos_a, pos_b,x,y,space, radius = 5):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (x, y)
    shape = pymunk.Segment(body, pos_a, pos_b, radius)

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

    index = f"ARROW_{body.id}"
    # players[2].inventory.pop(index)
    # space.remove(shape_b, body)

    return True


class Game:
    def __init__(self,screen:pg.Surface):
        self.screen = screen
        self.image =  pg.Surface(screen.get_size())

        self.space = pymunk.Space()
        self.space.gravity = (0, 980)

        self.player = Player(100,100, self.space)
        self.player.add_item_to_inventory_without_space("arc",Arc(100,self.image, self.player))


        self.space.add(self.player.body, self.player.shape)
        height = screen.get_size()[1]
        width = screen.get_size()[0]

        create_floor(pos_a=(0,0), pos_b=(width,0),x=0,y=height, space= self.space)
        create_floor(pos_a=(0,0), pos_b=(0,height),x=0,y=0, space= self.space)
        create_floor(pos_a=(0,0), pos_b=(0,-height),x=width,y=height, space= self.space)

        #platform
        create_floor(pos_a=(0,0), pos_b=(100,0),x=300,y=700, space= self.space, radius=20)
        create_floor(pos_a=(0,0), pos_b=(100,0),x=500,y=600, space= self.space, radius=20)
        create_floor(pos_a=(0,0), pos_b=(100,0),x=700,y=500, space= self.space, radius=20)
        create_floor(pos_a=(0,0), pos_b=(100,0),x=900,y=400, space= self.space, radius=20)
        create_floor(pos_a=(0,0), pos_b=(100,0),x=700,y=300, space= self.space, radius=20)
        create_floor(pos_a=(0,0), pos_b=(100,0),x=500,y=200, space= self.space, radius=20)
        create_floor(pos_a=(0,0), pos_b=(100,0),x=300,y=100, space= self.space, radius=20)


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


        self.time_change_start = 0
        self.time_change_end = 0




    def update(self):
        """ Update Game"""

        self.player.update()
        self.space.step(1 / 60.0)



    def draw(self):
        """ Draw the player and scene. """
        self.image.fill((0,0,0))
        self.player.draw(self.image)

        # Draw the floor
        # for shape in self.space.shapes:
        #     if isinstance(shape, pymunk.Segment):
        #         pg.draw.line(self.screen, (250, 250, 250), shape.body.position, (800,200), 5)


        self.space.debug_draw(self.draw_options)


        self.scale = pg.transform.scale(self.image, (self.image.get_width() * self.zoom_level, self.image.get_height() * self.zoom_level))

        # Calcular el desplazamiento basado en la posición del jugador
        offset_x = self.player.rect.x - (self.screen.get_width() // 2)
        offset_y = self.player.rect.y + (self.screen.get_height() // 2)  # Ajuste para la coordenada Y invertida

        # Dibujar la imagen escalada en la pantalla con los desplazamientos calculados
        self.screen.blit(self.scale, (-offset_x * (self.zoom_level - 1), -offset_y * (self.zoom_level - 1)))


    def __str__(self):
        return "Game Test"