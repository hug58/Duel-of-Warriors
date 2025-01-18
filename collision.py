from components.player import Player


class Collision:
    def __init__(self, player: Player, floor: int):
        self.player = player
        self.floor = floor


    def update(self):
        self.gravity()


    def gravity(self):


        if self.player.rect.bottom >= self.floor:
            if self.player.rect.bottom > self.floor:
                self.player.rect.bottom = self.floor

            if self.player.rect.bottom == self.floor and self.player.vly > 0:
                self.player.vly = 0
                self.player.jump_on = True



        else:
            self.player.vly += Player.GRAVITY
            self.player.jump_on = False
