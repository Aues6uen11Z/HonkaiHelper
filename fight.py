from airtest.core.api import *
import random


# 普通攻击
def A():
    times = random.randint(5, 10)
    for _ in range(times):
        device().key_press("J")
        device().key_release("J")
        sleep(random.uniform(0.1, 0.5))


# 必杀
def B():
    device().key_press("I")
    device().key_release("I")


# 武器/关卡技能
def weapon(choose=False):
    if choose:
        device().key_press("U")
        device().key_press("U")
    else:
        device().key_press("F")
        device().key_press("F")


# 分支攻击
def branch():
    device().key_press("J")
    sleep(random.uniform(1.5, 3))
    device().key_release("J")


# 随机移动
def move():
    orientation = ["W", "A", "S", "D"]
    index = random.randint(1, 4)
    device().key_press(orientation[index])
    sleep(random.uniform(0.5, 1))
    device().key_release(orientation[index])


# 概率抽取
def random_pick(atk_list, probabilities):
    x = random.uniform(0, 1)
    cumulative_probability = 0.0
    for item, item_probability in zip(atk_list, probabilities):
        cumulative_probability += item_probability
        if x < cumulative_probability:
            break
    return item


# 随机抽取一个动作, 根据自己角色改合适比例
def action():
    atk_list = [A, B, weapon, branch, move]
    probabilities = [0.8, 0, 0, 0.1, 0.1]
    random_pick(atk_list, probabilities)()


# 黑希连招
def combo():
    branch()
    sleep(random.uniform(0.3, 1.0))
    A()
    sleep(random.uniform(4.0, 6.0))
    weapon()
    sleep(random.uniform(1.0, 2.0))
    B()
    sleep(random.uniform(1.0, 1.5))
    A()

