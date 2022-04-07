import random

def move(direction:tuple):
    # return [0,0]
    if random.random()>0.95:
        if random.random()>0.5:
            dis=1
        else:
            dis=-1
        if random.random()>0.5:
            return [dis,0]
        else:
            return [0,dis]
    else:
        return direction
def gunpos():
    # return False
    return random.random()>0.3