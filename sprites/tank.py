from .abs_sprite import AbsSparite
import pygame as pg
from attrs import TankAttr
from utils import load_image,crossArea,load_sound
from .effects import TankBirth,TankHat,BigExplode,SmallExplode
from functools import reduce
from .terrain import Terrain

#子弹类
class Bullet(AbsSparite):
    imgFile='bullet.png'
    bullets=pg.sprite.Group()

    @classmethod
    def bulletSetOff(cls):
        for bt1, bt2s in dict(pg.sprite.groupcollide(EnemyTank.bullets, PlayerTank.bullets, False, False)).items():
            bt1.hit(False)
            bt2s[0].hit(False)
    @classmethod
    def groupUpdate(cls):
        cls.bulletSetOff()

    def __init__(self,emitter:'Tank',center:tuple,direction:tuple,speed:int,power:int,*groups):
        super().__init__(self.bullets,*groups)
        self.speed=speed
        self.power=power
        self.center=center
        self.direction=direction
        if direction[0]>0:
            angle=-90
        elif direction[0]<0:
            angle=90
        elif direction[1]>0:
            angle=180
        else:
            angle=0
        self.image=pg.transform.rotate(load_image(self.imgFile,True),angle)
        self.rect=self.image.get_rect()
        self.rect.center=center
        #发射器是谁
        self.emitter=emitter
    def update(self):
        center=self.rect.center
        self.rect=self.rect.clamp(self.mapRect)
        #检测是是否击中其他物体
        for group in [Terrain.terranins,PlayerTank.tanks,EnemyTank.tanks]:
            ls=pg.sprite.spritecollide(self,group,False)
            for i in ls:
                i.getShot(self)
                if isinstance(i,Tank):
                    break

        if center!=self.rect.center:
            self.hit()
            return

        # #检测子弹间的抵消
        # ls=pg.sprite.spritecollide(self,self.bullets,False)
        # for i in ls:
        #     if i is not self and type(self.emitter)!=type(i.emitter):
        #         self.hit(False)
        #         i.hit(False)

        # 沿着前进方向冲
        self.rect.move_ip(*[i * self.speed for i in self.direction])
        # 如果撞到边缘则毁灭
        # if not self.mapRect.inflate(-30, -30).colliderect(self.rect):
        #     self.hit()

    #击中
    def hit(self,explode:bool=True,kill:bool=True):
        if self.alive():
            if explode:
                center=list(self.rect.center)
                # if self.direction==[1,0]:
                #     center[0]+self.rect.width
                # elif self.direction==[-1,0]:
                #     center[0]-=self.rect.width
                # elif self.direction==[0,1]:
                #     center[1]+=self.rect.height
                # else:
                #     center[1]-=self.rect.height
                SmallExplode(center)
                self.kill()
            if kill:
                self.kill()


#检测精灵中某属性值是否大于0，若某属性为真，被装饰的类方法将失效
def chickStatus(*attrs:str):
    def decorator(func):
        return lambda *args,**kwargs:func(*args,**kwargs) if not any([getattr(args[0],i) for i in attrs]) else None
    return decorator

#坦克基础类
class Tank(AbsSparite):
    tanks=pg.sprite.Group()
    rectSize=(48,48)
    bullets=pg.sprite.Group()
    # 定住
    timing = 0
    # 设置定时
    @classmethod
    def setTiming(cls, timing: int):
        cls.timing = timing
    @classmethod
    def classUpdate(cls,*args,**kwargs):
        if cls.timing:
            cls.timing-=1
    def __init__(self,attr:TankAttr,leftTop:tuple):
        super().__init__(self.tanks)
        self.attr=attr
        self.image = attr.image
        self.direction=(0,1)
        self.level=0
        # self.rect=pg.Rect(0,0,*self.rectSize)
        self.rect=self.image.get_rect()
        # self.rect=pg.Rect(*leftTop,*self.rectSize)
        self.rect.topleft=leftTop
        self.invincible=0
        # self.bullets=pg.sprite.Group()
        #是否初生态
        self.isNascency=30
        # self.image.set_alpha(0)
        #出生态动画
        TankBirth(self.rect.center, self.isNascency)
        self.__chickToHit()
    def __chickToHit(self):
        pg.sprite.spritecollide(self,Terrain.terraninsObs,True)

    #@chickNascency
    @chickStatus("isNascency",'timing')
    def move(self, direction,*groups):
        if direction[0] or direction[1]:
            #如果移动方向和之前不一致
            if direction[0]!=self.direction[0] or direction[1] !=self.direction[1]:
                #旋转surface
                if abs(self.direction[0]-direction[0])>1 or abs(self.direction[1]-direction[1])>1:
                    angle=180
                elif direction[0]:
                    if direction[0]>0:
                        angle=self.direction[1]*90
                    else:
                        angle=-self.direction[1]*90
                else:
                    if direction[1]>0:
                        angle=-self.direction[0]*90
                    else:
                        angle=self.direction[0]*90
                self.image=pg.transform.rotate(self.image,angle)
                left,top=self.rect.left,self.rect.top

                self.rect = self.image.get_rect()
                if angle!=180:
                    size=Terrain.getImageSize()[0]
                    if direction[0]:
                        top = int(round(top / size))
                        top*=size
                    else:
                        left = int(round(left/size))
                        left *= size
                self.rect.top=top
                self.rect.left=left
                self.direction = direction
            else:
                direction=[i*self.attr.speed for i in direction]
                rect=self.rect
                self.rect=self.rect.move(*direction)
                #碰撞检测
                spritecollide=[pg.sprite.spritecollide(self,i,False) for i in groups]
                spritecollide=reduce(lambda x,y:x+y,spritecollide)
                if self in spritecollide:
                    spritecollide.remove(self)
                if spritecollide:
                    #检测移动前是否碰撞
                        #获取碰撞编号
                    rects=rect.collidelistall([i.rect for i in spritecollide])
                        #通过编号获取rect
                    rects = [[i.rect for i in spritecollide][i] for i in rects]
                    if rects and (crossArea(rect, rects) < crossArea(self.rect, [i.rect for i in spritecollide])):
                        self.rect = rect
                    elif not rects:
                        # self.rect=rect
                        for i in range(self.attr.speed):
                            _rect=rect.move(self.direction)
                            if(_rect.collidelistall([i.rect for i in spritecollide])):
                                break
                            rect=_rect
                        self.rect=rect
                #撞墙检测
                self.rect = self.rect.clamp(self.mapRect)
    #设置无敌
    def setInvincible(self,duration:int=100):
        if not self.invincible:
            TankHat(self)
        self.invincible=duration

    @chickStatus('isNascency')
    def getShot(self,bullet:Bullet):
        bullet.hit(not self.invincible)
        if not self.invincible:
            self.attr.life-=1
            if self.attr.life<1:
                self.explode()
                return self

    def explode(self):
        self.kill()
        BigExplode(self.rect.center)
        load_sound("bang.wav").play()
    def update(self):
        self.chickInvincible()
    #检查无敌状态
    def chickInvincible(self):
        if self.isNascency:
            self.isNascency-=1
            if not self.isNascency:
                self.image.set_alpha(255)
            else:
                self.image.set_alpha(0)
        elif self.invincible:
            #TODO 显示无敌
            self.invincible-=1
    #发射子弹
    @chickStatus('timing','isNascency')
    def gunpos(self):
        #判断发射冷却
        if len(self.bullets)>=self.attr.bulletNum:
            return
        #根据坦克方向获取发射坐标
        if self.direction[0]>0:
            pos=self.rect.midright
        elif self.direction[0]<0:
            pos=self.rect.midleft
        elif self.direction[1]>0:
            pos=self.rect.midbottom
        else:
            pos=self.rect.midtop
        #发射子弹
        Bullet(self,pos,self.direction,self.attr.bulletSpeed,self.attr.bulletPower,self.bullets)


class PlayerTank(Tank):
    tanks = pg.sprite.Group()
    bullets = pg.sprite.Group()
    def __init__(self,leftTop:tuple,playerNum:int=1,level=0):
        attr = self.configure.tank.getPlayerAttr(playerNum)
        attr=TankAttr(*attr)
        super().__init__(attr,leftTop)
        self.direction=(0,-1)
        self.killed=[]
        self.setInvincible()
        self.collection=None
        if level:
            self.upgrade(level)
    def __upgrade(self):
        self.level+=1
        if self.level==1:
            self.attr.bulletSpeed*=3
        elif self.level==2:
            self.attr.bulletNum+=1
        elif self.level==3:
            self.attr.bulletPower+=1
        else:
            return
        img = self.configure.tank.getPlayerLevelImg(self.level)
        image=load_image(img)
        if self.direction[0]:
            angle=-90*self.direction[0]
        elif self.direction[1]>0:
            angle=180
        else:
            angle=0
        self.image=pg.transform.rotate(image,angle)
    def upgrade(self,grade:int=1):
        for i in range(grade):
            self.__upgrade()
    def getShot(self,bullet:Bullet):
        if type(bullet.emitter)!=type(self):
            super().getShot(bullet)
        else:
            #TODO 定住不能动
            pass
    def setCollection(self,collection):
        self.collection=collection


class EnemyTank(Tank):
    tanks = pg.sprite.Group()
    bullets = pg.sprite.Group()
    def __init__(self,leftTop:tuple,_type:str):
        attr=self.configure.tank.getEnemysAttr(_type)
        attr=TankAttr(*attr)
        super().__init__(attr,leftTop)
        self.direction=(0,1)
    def update(self):
        super().update()
        if self.attr.life>1:
            #TODO 变色
            pass
    def getShot(self,bullet:Bullet):
        if type(self)!=type(bullet.emitter):
            super().getShot(bullet)
