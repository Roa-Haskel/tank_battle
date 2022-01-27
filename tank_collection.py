from sprites import PlayerTank,EnemyTank,Terrain
import computer_solve
from controller import Controller

class Player:
    def __init__(self,life:int=3,level:int=1,num:int=1,controller:Controller=None):
        self.life=life
        self.killList=dict()
        self.level=level
        self.num=num
        self.tank=self.createTank()
        self.controller=controller
    def addLife(self):
        self.life+=1
    def update(self):
        #死亡有命再生
        if not self.tank.alive() and self.life>0:
            self.life-=1
            self.tank=self.createTank()
        if self.tank.alive() and self.controller:
            dis,gunpos=self.controller.getInstructions()
            self.tank.move(dis,EnemyTank.tanks,PlayerTank.tanks,Terrain.terraninsObs)
            if gunpos:
                self.tank.gunpos()
        #分数记录
    def createTank(self):
        tank=PlayerTank((0,0),self.num)
        tank.setCollection(self)
        return tank

class Enemy:
    def __init__(self,tankList:list,maxNum:int=6):
        self.tankList=list(reversed(tankList))
        self.positions=[(0,0),(300,0),(500,0)]
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



