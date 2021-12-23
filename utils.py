import pygame as pg
import os

imageBasePath=os.path.join(os.path.dirname(__file__),"resources","images")
soundBasePath=os.path.join(os.path.dirname(__file__),"resources","sound")

def load_image(file,alpha=True):
    """loads an image, prepares it for play"""
    file=os.path.join(imageBasePath,file)
    try:
        surface = pg.image.load(file)
        surface=pg.transform.scale(surface,[int(i*1.5) for i in surface.get_size()])
    except pg.error:
        raise SystemExit('Could not load image "%s" %s' % (file, pg.get_error()))
    try:
        return surface.convert_alpha() if alpha else surface.convert()
    except:
        return surface

def load_images(path,alpha=True):
    return [load_image(os.path.join(path,i),alpha) for i in sorted(os.listdir(os.path.join(imageBasePath,path)))]


def load_sound(name):
    class NoneSound:
        def play(self):
            pass

    if not pg.mixer or not pg.mixer.get_init():
        return NoneSound()

    fullname = os.path.join(soundBasePath, name)
    sound = pg.mixer.Sound(fullname)

    return sound

def crossArea(rect:pg.Rect,rects:list)->int:
    return sum([i[0]*i[1] for i in [rect.clip(i).size for i in rects]])
