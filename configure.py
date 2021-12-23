import configparser
import os

class _Configure:
    def __init__(self):
        self.conf=configparser.ConfigParser()
        file = os.path.join(os.path.dirname(__file__), 'conf', 'configs')
        self.conf.read(file,encoding='utf-8')
        self.effects=self.__effects()
        self.tank=self.__tank()
        self.terrains=self.__terrains()
        self.level=self.__level()
        self.foods=self.__foods()
    @staticmethod
    def attrParser(attrStr):
        return [int(i) if i.isnumeric() else i for i in attrStr.split(",")]
    def __tank(self):
        class TankConf:
            @classmethod
            def getPlayerAttr(cls,playerNum:int=1):
                attr=self.conf.get("players","attr")
                player=self.conf.get("players","player1") if playerNum==1 else self.conf.get("players","player2")
                return self.attrParser(attr)+[player]
            @classmethod
            def getPlayerLevelImg(cls,level:int):
                key = 'level%s' % level
                return self.conf.get("players", key)
            @classmethod
            def getEnemysAttr(cls,_type:str):
                attr = self.conf.get("enemys", _type)
                return self.attrParser(attr)
        return TankConf
    def __effects(self):
        class Effects:
            explodeImgs=self.conf.get("effects",'explode')
            tankBirthImgs=self.conf.get("effects",'tank_birth')
        return Effects
    def __terrains(self):
        class Terrains:
            @classmethod
            def getAttr(cls,_type:str):
                attr=self.conf.get("terrains",_type.strip())
                return self.attrParser(attr)
        return Terrains
    def __level(self):
        class Level:
            @classmethod
            def getLevel(cls,level:int):
                return os.path.join(os.path.dirname(__file__),self.conf.get("level","path"),str(level)+".level")
        return Level
    def __foods(self):
        class Food:
            clock=self.conf.get("foods","clock")
            bomb=self.conf.get("foods","bomb")
            star=self.conf.get("foods","star")
            hat=self.conf.get("foods","hat")
            shovel=self.conf.get("foods","shovel")
            tank=self.conf.get("foods","tank")
            life=int(self.conf.get('foods','life'))
        return Food



configure=_Configure()

if __name__ == '__main__':
    attr = _Configure()
    # print(attr.terrains.getAttr('s'))
    print(attr.terrains.getAttr('s'))