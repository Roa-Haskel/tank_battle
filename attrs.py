from utils import load_image

"""
    定义坦克属性类，包含以下基本属性：
        生命值
        移动速度
        子弹速度
        子弹数量
        子弹威力
        图像
"""
class TankAttr:
    def __init__(
            self,life:int,
                 speed:int,
                 bulletSpeed:int,
                 bulletNum:int,
                 bulletPower:int,
                 image:str
    ):
        self.life=life
        self.speed=speed
        self.bulletSpeed=bulletSpeed
        self.bulletNum=bulletNum
        self.bulletPower=bulletPower
        self.image=load_image(image,True)