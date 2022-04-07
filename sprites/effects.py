from .abs_sprite import AbsSparite,_configure as configure
from utils import load_images,BaseImage
from pygame import transform

class Effects(AbsSparite):
    #图片配置
    images=""
    size=1
    def __init__(self,center:tuple,duration=0):
        super().__init__()
        self.images=BaseImage.getLocals(*self.images)
        if self.size!=1:
            size = [i * self.size for i in self.images[0].get_size()]
            self.images = [transform.scale(i, size) for i in self.images]
        self.image=self.images[0]
        self.rect=self.image.get_rect()
        self.rect.center=center
        #寿命
        self.duration= len(self.images) if not duration else duration
        self.age=0
    def animation(self):
        self.image=self.images[int((self.clock.get_time()-self.birthday)/1)%len(self.images)]
        self.image=self.images[int(self.age/1)%len(self.images)]
    def update(self):
        self.animation()
        self.duration-=1
        self.age+=1
        if not self.duration:
            self.kill()


# class Explode(Effects):
#     images = configure.effects.explodeImgs
#     def __init__(self,center:tuple,size=0.5):
#         super().__init__(center)
#         self.duration=len(self.images)
#         if size!=1:
#             self.images=[transform.scale(i,[int(j*size) for j in i.get_size()]) for i in self.images]
#             self.image=self.images[0]
#             self.rect=self.image.get_rect()
#             self.rect.center=center

class BigExplode(Effects):
    images = configure.effects.bigExplodeImgs
    # size = 1.8

class SmallExplode(Effects):
    images = configure.effects.smallExplodeImgs

class TankBirth(Effects):
    images = configure.effects.tankBirthImgs
    # size = 1.5


class TankHat(Effects):
    images=configure.effects.tankHat
    size=1.5
    def __init__(self,tank:'Tank'):
        self.tank=tank
        super().__init__(tank.rect.center,self.tank.invincible)
    def update(self):
        self.image.set_alpha(self.tank.image.get_alpha())
        self.duration=self.tank.invincible
        super().update()
        self.rect.center=self.tank.rect.center
        if not self.tank.alive():
            self.kill()


if __name__ == '__main__':
    TankBirth()
