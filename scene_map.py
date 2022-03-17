import numpy
from sprites import Terrain
import pygame as pg
# from window import Window
from configure import configure
from sprites.tank import Tank
import math

# class SceneMap(Window):

SPACE = 0
WIDTH = 26
HIGH = 26
TERRAIN_SIZE=Terrain.getImageSize()[0]
class SceneMap:
    width=WIDTH
    hight=HIGH
    space=SPACE
    mapSize=[width*TERRAIN_SIZE,hight*TERRAIN_SIZE]
    rect=[i * j + SPACE * (j - 1) for i, j in zip(Terrain.getImageSize(), [WIDTH, HIGH])]
    rect=pg.Rect(0,0,*rect)
    enemyPositionsIndex,playerPositionsIndex,homePositionsIndex=[
        [[0, 0], [12,0], [24,0]]
        ,[[8,24],[13,24]]
        ,[[11,22]]
    ]
    enemyPositions,playerPositions,homePositions=[
        # [[i[0] * WIDTH + SPACE * i[0], i[1] * HIGH + SPACE * i[1]] for i in arr]
        [[i[0] * TERRAIN_SIZE, i[1]*TERRAIN_SIZE] for i in arr]
        for arr in [enemyPositionsIndex,playerPositionsIndex,homePositionsIndex]]

    homePositions,homePositionsIndex=homePositions[0],homePositionsIndex[0]



    def __init__(self,level:int):
        self.mapArr=None
        path = configure.level.getLevel(level)
        self.mapArr=self.getMapData(path)
        self.enemyIndex=0
        self.initTerrains()
    def getMapData(self,file:str):
        with open(file) as f:
            data=f.read()
            data=data.split("\n")
            return [list(i) for i in data]
    # def removeOverlapMapData(self):
    #     for arr in self.enemyPositionsIndex + self.playerPositionsIndex:
    #         arr1=[math.ceil(i[0]/i[1]) for i in zip(Tank.rectSize,Terrain.getImageSize())]
    #         for i in range(arr[0],arr1[0]):
    #             for j in range(arr[1],arr1[1]):
    #                 self.mapArr[i][j]='0'
    # def getEnemyPosition(self):
    #     return self.enemyPositions[self.enemyIndex%len(self.enemyPositions)]

    def initTerrains(self):
        for i in range(len(self.mapArr)):
            for j in range(len(self.mapArr[0])):
                tp=self.mapArr[i][j]
                if tp!='0':
                    Terrain(tp,self.getPosition(j,i))

    def getPosition(self,x,y):
        size=Terrain.getImageSize()
        return [i * j + SPACE * (j - 1) for i, j in zip(size, [x, y])]
    def close(self):
        for i in Terrain.terranins:
            i.kill()
    def __enter__(self):
        self.initTerrains()
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()




if __name__ == '__main__':
    map = SceneMap(2)
    # map.removeOverlapMapData()
    for i in range(len(map.mapArr)):
        print([i for i in map.mapArr[i]])
    # SceneMap1()