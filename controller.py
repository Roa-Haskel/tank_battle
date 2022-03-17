import pygame as pg
import os
from configure import configure
# from pygame import joystick

pg.joystick.init()


class Controller:
    @classmethod
    def loop(cls):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                os._exit(0)
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                os._exit(0)

    def __init__(self,move=[pg.K_UP,pg.K_DOWN,pg.K_LEFT,pg.K_RIGHT],gunpos=pg.K_SPACE):
        self.move=[pg.__dict__[i] for i in configure.keyboard.direction]
        self.gunpos=gunpos
        pg.joystick.init()
        self.handle = [pg.joystick.Joystick(x) for x in range(pg.joystick.get_count())]
        if self.handle:
            self.handle=self.handle[0]
    def getInstructions(self):
        if self.handle:
            distence=self.handle.get_hat(0)
            distence=(distence[0],-distence[1])
            gunpos=any([self.handle.get_button(i) for i in range(4)])
        else:
            keystate = pg.key.get_pressed()
            if keystate[self.move[0]]:
                distence=(0,-1)
            elif keystate[self.move[1]]:
                distence=(0,1)
            elif keystate[self.move[2]]:
                distence=(-1,0)
            elif keystate[self.move[3]]:
                distence=(1,0)
            else:
                distence=(0,0)
            gunpos=True if keystate[self.gunpos] else False
        if all(distence):
            distence = (0, 0)
        return distence,gunpos