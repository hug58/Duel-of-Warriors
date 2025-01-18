""" Client and Single Game"""

import pygame as pg
import sys

from game import Game
from components.player import Player


def main():
    """ Client game of server"""
    pg.display.set_caption("Testing")
    clock = pg.time.Clock()
    WIDTH,HEIGHT = 800,200
    SCREEN = pg.display.set_mode((WIDTH,HEIGHT))
    game = Game(SCREEN)

    pg.joystick.init()
    joystick_count = pg.joystick.get_count()

    if joystick_count > 0:
        joystick = pg.joystick.Joystick(0)
        joystick.init()


    while True:
        for event in pg.event.get():

            if event.type == pg.QUIT:
                pg.quit()
                sys.exit(1)

            elif event.type == pg.JOYBUTTONDOWN:
                if event.button == 0:
                    pass

            elif event.type == pg.JOYAXISMOTION:
                if event.axis == 0 and event.value < 0:
                    game.player.move(-1)
                elif event.axis == 0 and event.value > 0:
                    game.player.move(1)
                else:
                    game.player.move_on = False

            elif event.type == pg.JOYBUTTONUP:
                if event.button == 0:
                    pass

            elif event.type == pg.KEYUP:
                if event.key == pg.K_a and game.player.move_on or event.key == pg.K_d and game.player.move_on:
                    game.player.body.velocity = (0, 0)

            elif event.type == pg.MOUSEBUTTONDOWN:
                game.player.actions("arc")

            if event.type == pg.MOUSEMOTION:
                game.player.angle_arc = event.pos

        keys = pg.key.get_pressed()
        if game.player.move_on:
            if keys[pg.K_a]:
                game.player.move(-1)
            elif keys[pg.K_d]:
                game.player.move(1)

        if keys[pg.K_SPACE]:
            if game.player.jump_on:
                game.player.jump()

        SCREEN.fill((0,0,0))
        game.update()
        game.draw()


        clock.tick(60)
        pg.display.flip()

if __name__ == "__main__":
    main()
