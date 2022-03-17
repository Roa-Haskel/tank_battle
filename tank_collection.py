from sprites import PlayerTank,EnemyTank,Terrain
import computer_solve
from controller import Controller
from scene_map import SceneMap

class Player:
    def __init__(self,life:int=3,level:int=0,num:int=1,controller:Controller=None):
        self.life=life
        self.killList=dict()
        self.level=level
        self.num=num
        self.position=SceneMap.playerPositions[num-1]
        self.tank=None
        self.controller=controller
        self.tankLevel=0
    def addLife(self):
        self.life+=1
    def update(self):
        #死亡有命再生
        if self.tank is None or (not self.tank.alive() and self.life>0):
            self.life-=1
            self.tank=self.createTank()
        if self.tank.alive() and self.controller:
            dis,gunpos=self.controller.getInstructions()
            if any(dis):
                self.tank.move(dis,EnemyTank.tanks,PlayerTank.tanks,Terrain.terraninsObs)
            if gunpos:
                self.tank.gunpos()
        #TODO 分数记录

    def createTank(self):
        tank=PlayerTank(self.position,self.num,level=self.level)
        self.level=3
        tank.setCollection(self)
        return tank
    def close(self):
        self.level = self.tank.level
        if self.tank.alive():
            self.tank.kill()
            self.tank=None
            self.life+=1

class Enemy:
    def __init__(self,tankList:list,maxNum:int=6):
        self.tankList=list(reversed(tankList))
        self.positions=SceneMap.enemyPositions
        self.index=0
        self.maxNum=maxNum
    def update(self):
        self.__opear()
        if len(EnemyTank.tanks)<self.maxNum and len(self.tankList)>0:
            num=len(self.positions)
            EnemyTank(self.positions[self.index%num],self.tankList.pop())
            self.index+=1
        return len(EnemyTank.tanks)>0
    def __opear(self):
        for t in EnemyTank.tanks:
            t.move(computer_solve.move(t.direction), EnemyTank.tanks,PlayerTank.tanks,Terrain.terraninsObs)
            if computer_solve.gunpos():
                t.gunpos()
        EnemyTank.classUpdate()
    def __len__(self):
        return len(self.tankList)+len(EnemyTank.tanks)



