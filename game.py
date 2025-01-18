#!/usr/bin/python3
""" this is the manager game """

import pygame as pg
import pymunk
import pymunk.pygame_util

from components.player import Player
from components.weapons import Arc



players = {

}

def create_floor(width,height, space):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (0, height)
    shape = pymunk.Segment(body, (-0, 0), (width, 0), 5)

    shape.friction = 1
    shape.collision_type = 1

    space.add(body, shape)

def collision_handler(arbiter, space: pymunk.Space, data):
    shape_a = arbiter.shapes[0]
    shape_b = arbiter.shapes[1].collision_type
    print(f"Collision detected between: {shape_a} and {shape_b}")
    player:Player = players[shape_b]
    player.jump_on = True
    player.move_on = True

    return True

class Game:
    def __init__(self,screen:pg.Surface):
        self.screen = screen
        draw_options = pymunk.pygame_util.DrawOptions(screen)


        self.space = pymunk.Space()
        self.space.gravity = (0, 900)

        self.player = Player(100,100, self.space)
        self.player.add_item_to_inventory_without_space("arc",Arc(screen, self.player))


        self.space.add(self.player.body, self.player.shape)

        create_floor(screen.get_size()[0],screen.get_size()[1], self.space)

        # Set up collision handler
        players[2] = self.player
        handler = self.space.add_collision_handler(1, 2)  # Assuming 1 for floor and 2 for player
        handler.begin = collision_handler

        self.count_inventory = len(self.player.inventory)

    def update(self):
        """ Update Game"""

        self.player.update()
        self.space.step(1 / 60.0)



    def draw(self):
        """ Draw the player and scene. """
        self.player.draw(self.screen)

        # Draw the floor
        for shape in self.space.shapes:
            if isinstance(shape, pymunk.Segment):
                pg.draw.line(self.screen, (250, 250, 250), shape.body.position, (800,200), 5)


    def __str__(self):
        return "Game Test"