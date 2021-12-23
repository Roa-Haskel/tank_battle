from sprites import PlayerTank,EnemyTank,Bullet,AbsSparite,Terrain
from sprites.food import foodRandom,Food
import pygame as pg
import os
import computer_solve
import random
from scene_map import SceneMap
from utils import load_sound

SCREENRECT = pg.Rect(0, 0, *SceneMap.mapSize)


if __name__ == '__main__':
    if pg.get_sdl_version()[0] == 2:
        pg.mixer.pre_init(44100, 32, 2, 1024)
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


    player2=PlayerTank([500,600],2)

    tank=PlayerTank((300,500))
    # tank.upgrade()
    # tank.upgrade()
    # tank.upgrade()

    foodRandom([200,200])

    for i in range(3):
        EnemyTank((5 * i, 0), random.sample(['a', 'b'], 1)[0])

    sc=SceneMap(1)
    sc.removeOverlapMapData()
    sc.initTerrains()

    startSound=load_sound("start.wav")
    start=1


    while True:
        if start:
            startSound.play()
            start=0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                os._exit(0)
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                os._exit(0)
        keystate = pg.key.get_pressed()
        if keystate[pg.K_UP]:
            distence=(0,-1)
        elif keystate[pg.K_DOWN]:
            distence=(0,1)
        elif keystate[pg.K_LEFT]:
            distence=(-1,0)
        elif keystate[pg.K_RIGHT]:
            distence=(1,0)
        else:
            distence=(0,0)

        AbsSparite.allSprites.clear(screen,bg)

        if tank.alive():
            tank.move(distence,EnemyTank.tanks,PlayerTank.tanks,Terrain.terraninsObs)

        if keystate[pg.K_SPACE] and tank.alive():
            tank.gunpos()

        for t in EnemyTank.tanks:
            t.move(computer_solve.move(t.direction), EnemyTank.tanks,PlayerTank.tanks,Terrain.terraninsObs)
            if computer_solve.gunpos():
                t.gunpos()
                pass
        if 0:
            player2.move(computer_solve.move(player2.direction),EnemyTank.tanks,PlayerTank.tanks,Terrain.terraninsObs)
            if computer_solve.gunpos():
                player2.gunpos()

        Bullet.chickCollision(PlayerTank.tanks,EnemyTank.tanks,Terrain.terranins)
        Bullet.chickSetOff()

        if not tank.alive():
            tank=PlayerTank((100,300))
        if not player2.alive():
            player2=PlayerTank([500,300],2)
        if random.random()>0.99 and len(EnemyTank.tanks)>-1:
            EnemyTank([random.randint(0,SceneMap.mapSize[0]-32),random.randint(0,SceneMap.mapSize[1]-32)],random.sample(['a','b'],1)[0])
        if random.random()>0.99 and len(Food.foods)==0:
            foodRandom((random.randint(0,500),random.randint(0,500)))

        EnemyTank.classUpdate()

        AbsSparite.allSprites.update()
        dirty = AbsSparite.allSprites.draw(screen)
        pg.display.update(dirty)
        clock.tick(24)
