from pygame.transform import rotate
from pygame.sprite import Group
from pygame.sprite import collide_rect,groupcollide
from .abs_sprite import AbsSparite
from .effects import Explode
from utils import load_image
import itertools

class Bullet(AbsSparite):
    imgFile='bullet.png'
    bullets=Group()

    #检测子弹击中其他东西
    @classmethod
    def chickCollision(cls,*groups):
        for group in groups:
            bulletEmps = groupcollide(cls.bullets, group,False,False)
            for b,es in bulletEmps.items():
                for e in es[:2]:
                    e.getShot(b)
                b.call()

    #检查子弹间碰撞抵消
    @classmethod
    def chickSetOff(cls):
        for i in itertools.product(cls.bullets,repeat=2):
            if i[0]==i[1]:
                continue
            if collide_rect(*i) and type(i[0].emitter)!=type(i[1].emitter):
                for j in i:
                    j.hit()

    def __init__(self,emitter:'Tank',center:tuple,direction:tuple,speed:int,power:int,*groups):
        super().__init__(self.bullets,*groups)
        self.speed=speed
        self.power=power
        self.center=center
        self.direction=direction
        self.life=2
        if direction[0]>0:
            angle=-90
        elif direction[0]<0:
            angle=90
        elif direction[1]>0:
            angle=180
        else:
            angle=0
        self.image=rotate(load_image(self.imgFile,True),angle)
        self.rect=self.image.get_rect()
        # self.rect.inflate_ip(10,10)
        # self.rect.size=[i*8 for i in self.rect.size]
        # self.rect.center=(center[0]+5,center[1]+5)
        self.rect.center=center
        #发射器是谁
        self.emitter=emitter
    def update(self):
        self.rect.move_ip(*[i*self.speed for i in self.direction])
        if not self.mapRect.inflate(-30,-30).colliderect(self.rect):
            self.hit()
    #击中
    def hit(self,explode:bool=True,life:int=2):
        self.life-=life
        if not self.life:
            self.kill()
        if explode:
            Explode(self.rect.center)
    def call(self):
        if self.life<2:
            Explode(self.rect.center)
            self.kill()




