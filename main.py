from sprites import AbsSparite,Bullet
from sprites.food import foodRandom,Food
import pygame as pg
from tank_collection import Player,Enemy
from controller import Controller
from scene_map import SceneMap
from utils import load_sound
import random
import os

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


    #播放关卡开始背景音乐
    startSound=load_sound("start.wav")

    #创建控制器
    controller=Controller()

    #创建player1
    player1=Player(3,0,controller=controller)

    #创建敌军坦克阵营
    ls=['a' for i in range(20)]
    for i in range(0,len(ls),2):
        ls[i]='b'

    #创建地图并初始化
    for i in range(1,33):
        with SceneMap(i) as scMp:
            startSound.play()
            enemy = Enemy(ls, 4)
            while player1.life>=0 and len(enemy):
                controller.loop()
                player1.update()
                enemy.update()
                Bullet.groupUpdate()

                #产生食物
                if len(Food.foods)<1:
                    foodRandom((random.randint(0,bg.get_size()[0]),random.randint(0,bg.get_size()[1])))

                #在画布上绘制精灵
                AbsSparite.allSprites.update()
                dirty = AbsSparite.allSprites.draw(screen)
                pg.display.update(dirty)
                AbsSparite.allSprites.clear(screen,bg)
                clock.tick(60)
            if player1.life<0:
                os._exit(0)
            print(player1.life)
            print("------------")
            player1.close()
