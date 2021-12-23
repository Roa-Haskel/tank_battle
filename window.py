import pygame as pg

SIZE=(640,480)

class Window:
    if pg.get_sdl_version()[0] == 2:
        pg.mixer.pre_init(44100, 32, 2, 1024)
    pg.init()
    screen = pg.display.set_mode(SIZE, 0, pg.display.mode_ok(SIZE, 0, 32))
    screen.blit(pg.Surface(SIZE), (0, 0))
    def show(self):
        pass


