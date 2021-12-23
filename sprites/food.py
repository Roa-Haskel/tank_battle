from .abs_sprite import AbsSparite
from .tank import PlayerTank,EnemyTank
import pygame as pg
from utils import load_image
from configure import configure
import random

class Food(AbsSparite):
    foods=pg.sprite.Group()
    def __init__(self,_type:str,center:tuple):
        self.image=load_image(_type)
        self.rect=self.image.get_rect()
        self.rect.center=center
        self.life=configure.foods.life
        super().__init__(self.foods)
    def update(self) -> None:
        ls=pg.sprite.spritecollide(self,PlayerTank.tanks,False)
        if ls:
            self.beEaten(ls[0])
            self.kill()
        self.life-=1
        if self.life%10>5:
            self.image.set_alpha(255)
        else:
            self.image.set_alpha(0)
        if self.life<1:
            self.kill()
    def beEaten(self,obj:PlayerTank=None):
        pass
    def disappear(self):
        self.life=0

class Star(Food):
    def __init__(self,center:tuple):
        super().__init__(configure.foods.star,center)
    def beEaten(self,obj:PlayerTank=None):
        obj.upgrade(1)

class TankLife(Food):
    def __init__(self,center:tuple):
        super().__init__(configure.foods.tank,center)
    def beEaten(self,obj:PlayerTank=None):
        #TODO 加命
        pass

class Hat(Food):
    def __init__(self,center:tuple):
        super().__init__(configure.foods.hat,center)
    def beEaten(self,obj:PlayerTank=None):
        #TODO 戴帽子
        obj.setInvincible(3000)

class Bomb(Food):
    def __init__(self,center:tuple):
        super().__init__(configure.foods.bomb,center)
    def beEaten(self,obj:PlayerTank=None):
        for i in EnemyTank.tanks:
            i.explode()

class Clock(Food):
    def __init__(self,center:tuple):
        super().__init__(configure.foods.clock,center)
    def beEaten(self,obj:PlayerTank=None):
        # obj.setTiming(3000)
        for i in EnemyTank.tanks:
            i.setTiming(3000)
class Shovel(Food):
    def __init__(self,center:tuple):
        super().__init__(configure.foods.shovel,center)
    def beEaten(self,obj:PlayerTank=None):
        #TODO 家精装修
        pass

def foodRandom(center:tuple):
    return random.sample([Shovel,Hat,Clock,Bomb,TankLife,Star],1)[0](center)
    # return Star(center)
