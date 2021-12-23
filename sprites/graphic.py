from .abs_sprite import AbsSparite
from pygame import Surface
class Graphic(AbsSparite):
    def __init__(self,sprite:AbsSparite):
        draw.rect(,sprite.rect)
        Surface()