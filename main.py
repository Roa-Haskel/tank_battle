from sprites import AbsSparite
from sprites.food import foodRandom,Food
import pygame as pg
from tank_collection import Player,Enemy
from controller import Controller
from scene_map import SceneMap
from utils import load_sound
import random

SCREENRECT = pg.Rect(0, 0, *SceneMap.mapSize)

if __name__ == '__main__':
    if pg.get_sdl_version()[0] == 2:
        pg.mixer.pre_init(44100, 32, 2, 1024)

    #初始化pygame，生成窗口等
    pg.init()
    winstyle = 0
    bestdepth = pg.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pg.display.set_mode(SCREENRECT.size, winstyle, bestdepth)
    AbsSparite.setMapRect(screen.get_rect())
    #
    clock = pg.time.Clock()
    AbsSparite.setClock(clock)

    bg=pg.Surface(SCREENRECT.size)
    screen.blit(bg, (0, 0))

    #创建地图并初始化
    sc=SceneMap(1)
    sc.removeOverlapMapData()
    sc.initTerrains()

    #播放关卡开始背景音乐
    startSound=load_sound("start.wav")
    start=1

    #创建控制器
    controller=Controller()

    #创建player1
    player1=Player(3,1,controller=controller)

    #创建敌军坦克阵营
    ls=['a' for i in range(100)]
    for i in range(0,len(ls),2):
        ls[i]='b'
    enemy=Enemy(ls,4)
    startSound.play()
    while player1.life:

        controller.loop()
        player1.update()
        enemy.update()

        #产生食物
        if len(Food.foods)<1:
            foodRandom((random.randint(0,bg.get_size()[0]),random.randint(0,bg.get_size()[1])))

        #在画布上绘制精灵
        AbsSparite.allSprites.update()
        dirty = AbsSparite.allSprites.draw(screen)
        pg.display.update(dirty)
        AbsSparite.allSprites.clear(screen,bg)
        clock.tick(24)

