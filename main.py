import sys
import pygame as pg
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *

class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        pg.event.set_grab(True)
        #self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.shot_global_event = pg.USEREVENT + 0
        self.melee_global_event = pg.USEREVENT + 1
        pg.time.set_timer(self.shot_global_event, 40)
        pg.time.set_timer(self.melee_global_event, 20)
        self.new_game()


    def new_game(self):
        self.player = Player(self)
        self.map = Map(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)

    def update(self):
        self.raycasting.update()
        self.object_handler.update()
        self.player.update()
        self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        # self.screen.fill("black")
        self.object_renderer.draw()
        self.weapon.draw()
        # self.map.draw()
        # self.player.draw()

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.shot_global_event:
                self.global_trigger = True
            self.player.shotgun_fire_event(event)
    #
    # def check_events(self):
    #     self.global_trigger = False
    #     for event in pg.event.get():
    #         if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
    #             pg.quit()
    #             sys.exit()
    #         elif event.type == pg.USEREVENT:
    #             if event.type == self.shot_global_event:
    #                 self.global_trigger = True
    #             self.player.shotgun_fire_event(event)
    #
    #         elif event.type == pg.USEREVENT:
    #             if event.type == self.melee_global_event:
    #                 self.global_trigger = True
    #             self.player.melee_attack_event(event)



    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

if __name__ == '__main__':
    game = Game()
    game.run()
