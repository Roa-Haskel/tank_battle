import pygame as pg
import os

class Controller:
    @classmethod
    def loop(cls):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                os._exit(0)
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                os._exit(0)

    def __init__(self,move=[pg.K_UP,pg.K_DOWN,pg.K_LEFT,pg.K_RIGHT],gunpos=pg.K_SPACE):
        self.move=move
        self.gunpos=gunpos

    def getInstructions(self):
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
        return distence,gunpos
