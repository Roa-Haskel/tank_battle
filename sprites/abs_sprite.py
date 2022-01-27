from pygame.sprite import Sprite,RenderUpdates
from pygame import Rect
from pygame.time import Clock
from configure import configure  as _configure


class AbsSparite(Sprite):
    mapRect = None
    configure=_configure
    clock:Clock=None
    @classmethod
    def setMapRect(cls, mapRect: Rect):
        cls.mapRect = mapRect
    @classmethod
    def setClock(cls,clock:Clock):
        cls.clock=clock
    allSprites=RenderUpdates()
    def __init__(self,*groups):
        super().__init__(self.allSprites,*groups)
        self.birthday=self.clock.get_time()

    #中弹后的回调方法
    def getShot(self,bullet):
        pass