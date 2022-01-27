from .abs_sprite import AbsSparite
from pygame.sprite import Group
from configure import configure
from utils import load_image
from pygame import transform,Rect
from sprites.effects import SmallExplode


#地形元素类，砖块、钢、树、冰、水
class Terrain(AbsSparite):
    class types:
        #砖头
        brick="b"
        #钢
        steel="s"
        #水
        water='w'
        #冰
        ice='i'
        #树
        tree='t'
    __terrainTypes=[i for i in dir(types) if not i.startswith("__")]
    imageSize=None
    @classmethod
    def getImageSize(cls):
        if not cls.imageSize:
            path = configure.terrains.getAttr(cls.types.brick)[0]
            cls.imageSize=load_image(path).get_size()
            # cls.imageSize=transform.scale(load_image(path),(1,1)).get_size()
            # cls.imageSize=[i*2 for i in cls.imageSize]
        return cls.imageSize

    @classmethod
    def createTerrain(cls,inx:int=0):
        return cls(cls.__terrainTypes[inx])
    terranins=Group()
    terraninsObs=Group()
    def __init__(self,_type:str,leftTop:tuple):
        attr=configure.terrains.getAttr(_type)
        self.image=load_image(attr[0])
        self.image=transform.scale(load_image(attr[0]),self.imageSize)
        #可摧毁 、可阻碍
        self.destroy,self.obstacle=attr[1:]
        self.rect=self.image.get_rect()
        self.rect.topleft=leftTop
        self.type=_type
        if self.obstacle:
            super().__init__(self.terranins,self.terraninsObs)
        else:
            super().__init__(self.terranins)
    def getShot(self,bullet):
        if not self.destroy:
            return
        bullet.hit(True)
        # SmallExplode(self.rect.center)
        if bullet.power>self.destroy:
            self.kill()
        elif self.type==self.types.brick:
            self.destroy-=0.5
            #从子弹方向切割土
            x=self.rect.width/2
            if bullet.direction[0]>0:
                self.image=transform.chop(self.image,Rect(0,0,x,0))
                self.rect.move_ip(x,0)
            elif bullet.direction[0]<0:
                self.image = transform.chop(self.image, Rect(0, 0, x, 0))
            elif bullet.direction[1]>0:
                self.image=transform.chop(self.image,Rect(0,0,0,x))
                self.rect.move_ip(0,x)
            else:
                self.image=transform.chop(self.image, Rect(x, 0, 0, x))




