from .abs_sprite import AbsSparite,_configure as configure
from utils import load_images
from pygame import transform

class Effects(AbsSparite):
    #图片路径
    images=""
    def __init__(self,center:tuple,duration:int=-1):
        super().__init__()
        self.images = load_images(self.images)
        self.image=self.images[0]
        self.rect=self.image.get_rect()
        self.rect.center=center
        #寿命
        self.duration=duration
    def animation(self):
        self.image=self.images[int((self.clock.get_time()-self.birthday)/1)%len(self.images)]
    def update(self):
        self.animation()
        self.duration-=1
        if not self.duration:
            self.kill()


class Explode(Effects):
    images = configure.effects.explodeImgs
    def __init__(self,center:tuple,size=0.5):
        super().__init__(center)
        self.duration=len(self.images)
        if size!=1:
            self.images=[transform.scale(i,[int(j*size) for j in i.get_size()]) for i in self.images]
            self.image=self.images[0]
            self.rect=self.image.get_rect()
            self.rect.center=center
class TankBirth(Effects):
    images = configure.effects.tankBirthImgs

if __name__ == '__main__':
    TankBirth()
