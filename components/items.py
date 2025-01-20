import pygame as pg
import time
import os


TICK_RATE = 1/1



class Item(pg.sprite.Sprite):
    newid = 0
    def __init__(self,
                 route_img: str,
                 screen: pg.Surface,
                 count: int,
                 player: object
                 ):
        """
        :param route_img:
        :param screen:
        :param count:
        :param count_limit:
        :param player:
        """
        
        super().__init__()

        Item.newid += 1
        self.id = Item.newid
        self.player_id:object = player



        self.route_img =  route_img
        path_img = os.path.join(os.path.abspath("."), route_img)
        self.image = pg.image.load(path_img)
        self.rect = self.image.get_rect()
        self.tick_last_sent = time.time()
        self.screen = screen

        self.count_available = count
        self.count_item = count
        self.reload_action = False
        self.angle = 0

        self.body = None
        self.shape = None

        self.vlx = 0
        self.vly = 0

        self.time_reload = 200  #milliseconds
        self.time_init_reload = 0
        self.time_charge = 0


        self._visible = True

    def update(self):
        """
        :return:
        """

        if self.reload_action and self.count_item > 0:
            time_now = pg.time.get_ticks()

            if time_now - self.time_init_reload >= self.time_reload:
                self.reload()
                self.reload_action = False


        self.rect.x += self.vlx
        self.rect.y += self.vly

        self.can_show()


    def reload(self):
        if self.count_available <= 0:
            self.count_available = self.count_item


    def actions(self):
        """
        method to be defined in the child classes.

        :return:
        """
        pass


    def get_counter(self) -> int:
        """
        getting position in counter

        :return:
        """
        if self.count_available >= 1:
            self.count_available -= 1

            return self.count_available

        return -1


    def can_show(self):
        pass


    @property
    def visible(self):
        return self._visible
    

    @visible.setter
    def visible(self,status:bool):
        self._visible = status


    def draw(self):
        surface = self.image
        angle = self.angle % 360

        if angle != 0:
            surface = pg.transform.rotate(surface,angle)

        new_rect = surface.get_rect(center=self.rect.center)
        self.screen.blit(surface,  new_rect.topleft)


    def __str__(self):
        return self.route_img


