from datetime import datetime

from anti_detection import *
from config import *
from fight import *


# 登录前有可能要更新数据
def check_update():
    if exists(Template(r"img/tpl1646114198037.png", record_pos=(0.002, -0.129), resolution=(1277, 720))):
        find_click(Template(r"img/tpl1646114248108.png", record_pos=(0.0, 0.116), resolution=(1277, 720)))
        find_click(Template(r"img/tpl1646114570699.png", record_pos=(0.0, 0.048), resolution=(1277, 720)), timeout=1200)


# 回到主界面
def back_to_main():
    while True:
        if exists(Template(r"img/tpl1645854690653.png", record_pos=(0.23, 0.076), resolution=(1280, 720))):
            break
        elif exists(Template(r"img/tpl1645853249505.png", record_pos=(0.083, 0.248), resolution=(1280, 720))):
            find_click(Template(r"img/tpl1645853249505.png", record_pos=(0.083, 0.248), resolution=(1280, 720)))
            find_click(Template(r"img/tpl1645854410174.png", record_pos=(-0.001, 0.134), resolution=(1280, 720)))
        else:
            device().key_press("`")
            device().key_release("`")
        sleep(random.uniform(0.5, 1.0))


# 返回上一层
def back():
    device().key_press("`")
    device().key_release("`")
    sleep(random.uniform(0.3, 1.0))
    find_click(Template(r"img/tpl1646924632727.png", rgb=True, record_pos=(-0.106, 0.048), resolution=(1280, 720)), timeout=1)


# 刚上线的一系列操作
def login():
    # 点击登录
    wait(Template(r"img/tpl1645854935043.png", record_pos=(0.407, 0.234), resolution=(1280, 720)), timeout=1200,
         interval=3,
         intervalfunc=check_update)
    random_click(590, 300, 1160, 540, times=3)

    sleep(10)
    # 关闭公告和活动
    back_to_main()


# 戳老婆
def lsp():
    back_to_main()
    for _ in range(random.randint(1, 5)):
        find_click(Template(r"img/tpl1646118716275.png", rgb=True, record_pos=(-0.098, -0.17), resolution=(1280, 720)))
        find_click(Template(r"img/tpl1646228840476.png", record_pos=(-0.098, -0.168), resolution=(1280, 720)))
        sleep(10)


# 领金币
def gold():
    if exists(Template(r"img/tpl1645854690653.png", record_pos=(0.23, 0.076), resolution=(1280, 720))):
        find_click(Template(r"img/tpl1645856299732.png", record_pos=(0.325, 0.248), resolution=(1280, 720)))
    find_click(Template(r"img/tpl1645878953544.png", record_pos=(-0.195, -0.062), resolution=(1280, 720)))


# 取体力
def strength():
    if exists(Template(r"img/tpl1645854690653.png", record_pos=(0.23, 0.076), resolution=(1280, 720))):
        find_click(Template(r"img/tpl1645856299732.png", record_pos=(0.325, 0.248), resolution=(1280, 720)))

    find_click(Template(r"img/tpl1646407737965.png", record_pos=(-0.336, -0.067), resolution=(1280, 720)))
    find_click(Template(r"img/tpl1646229280900.png", record_pos=(0.09, 0.156), resolution=(1280, 720)))
    sleep(5)
    device().key_press("`")
    device().key_release("`")


# 远征
def expedition():
    # 打开远征界面
    if exists(Template(r"img/tpl1645854690653.png", record_pos=(0.23, 0.076), resolution=(1280, 720))):
        find_click(Template(r"img/tpl1645856299732.png", record_pos=(0.325, 0.248), resolution=(1280, 720)))
    find_click(Template(r"img/tpl1645856952234.png", record_pos=(0.17, 0.245), resolution=(1280, 720)))

    # 领前一天远征奖励
    if find_click(Template(r"img/tpl1645857277604.png", record_pos=(0.237, -0.089), resolution=(1280, 720))):
        find_click(Template(r"img/tpl1645857505405.png", record_pos=(-0.001, 0.145), resolution=(1280, 720)))

    # 挂远征
    for _ in range(expedition_times):
        if not exists(
                Template(r"img/tpl1646229453843.png", threshold=0.7, rgb=False, record_pos=(0.237, -0.088),
                         resolution=(1280, 720))):
            # 滑动远征列表
            p1 = random_coordinate(540, 640, 960, 100)
            p2 = random_coordinate(540, 300, 960, 100)
            swipe(p1, p2)
        if find_click(Template(r"img/tpl1646229453843.png", threshold=0.7, rgb=False, record_pos=(0.237, -0.088),
                               resolution=(1280, 720))):
            find_click(
                Template(r"img/tpl1645857954430.png", rgb=True, record_pos=(0.118, 0.228), resolution=(1280, 720)))
            find_click(
                Template(r"img/tpl1645857986323.png", rgb=True, record_pos=(0.362, 0.227), resolution=(1280, 720)))

    # 返回家园界面
    sleep(3)
    device().key_press("`")
    device().key_release("`")


# 打工
def work():
    # 打开打工界面
    if exists(Template(r"img/tpl1645854690653.png", record_pos=(0.23, 0.076), resolution=(1280, 720))):
        find_click(Template(r"img/tpl1645856299732.png", record_pos=(0.325, 0.248), resolution=(1280, 720)))
    find_click(Template(r"img/tpl1645865941303.png", record_pos=(0.295, 0.25), resolution=(1280, 720)))

    if exists(Template(r"img/tpl1645866078753.png", record_pos=(0.483, 0.0), resolution=(1280, 720))):
        find_click(Template(r"img/tpl1645866078753.png", record_pos=(0.483, 0.0), resolution=(1280, 720)))

    # 领打工奖励
    random_click(wx, wy, ww, wh, 15)

    # 打工派遣
    for _ in range(6):
        find_click(Template(r"img/tpl1645868275668.png", rgb=True, record_pos=(0.181, 0.246), resolution=(1280, 720)))
        find_click(Template(r"img/tpl1645868302799.png", rgb=True, record_pos=(0.388, 0.246), resolution=(1280, 720)))
        random_click(wx, wy, ww, wh)

    # 返回家园界面
    find_click(Template(r"img/tpl1645868275668.png", rgb=True, record_pos=(0.181, 0.246), resolution=(1280, 720)))
    sleep(3)
    for _ in range(2):
        device().key_press("`")
        device().key_release("`")
        sleep(0.5)


# 商店必买品
def shop():
    # 打开商店页面
    if exists(Template(r"img/tpl1645854690653.png", record_pos=(0.23, 0.076), resolution=(1280, 720))):
        find_click(Template(r"img/tpl1645856299732.png", record_pos=(0.325, 0.248), resolution=(1280, 720)))
    find_click(Template(r"img/tpl1646117052091.png", record_pos=(0.44, 0.246), resolution=(1274, 720)))

    # 金币商品
    find_click(Template(r"img/tpl1646117309518.png", record_pos=(-0.405, -0.13), resolution=(1280, 720)))
    p1 = random_coordinate(850, 600, 800, 100)
    p2 = random_coordinate(850, 300, 800, 100)
    swipe(p1, p2)
    while find_click(
            Template(r"img/tpl1646117620315.png", rgb=True, record_pos=(0.052, 0.239), resolution=(1280, 720))):
        find_click(Template(r"img/tpl1646117704059.png", threshold=0.5, rgb=True, record_pos=(0.198, 0.16),
                            resolution=(1280, 720)))
        find_click(Template(r"img/tpl1646229023628.png", record_pos=(0.134, 0.116), resolution=(1280, 720)), timeout=1)
        sleep(3)

    # 每周时序通行证
    if datetime.today().weekday() == 0:
        find_click(Template(r"img/tpl1646117961571.png", record_pos=(-0.409, 0.166), resolution=(1280, 720)))
        find_click(Template(r"img/tpl1646117979667.png", record_pos=(-0.407, 0.171), resolution=(1280, 720)))
        find_click(Template(r"img/tpl1646117999435.png", record_pos=(-0.224, 0.065), resolution=(1280, 720)))
        find_click(Template(r"img/tpl1646118020115.png", record_pos=(0.198, 0.161), resolution=(1280, 720)))

    # 返回家园界面
    sleep(3)
    device().key_press("`")
    device().key_release("`")


# 每日活跃
def daily(last=False):
    # 打开每日界面
    back_to_main()
    find_click(Template(r"img/tpl1645871324073.png", record_pos=(-0.46, -0.186), resolution=(1280, 720)))
    random_click(100, 170, 180, 60)
    if find_click(Template(r"img/tpl1646925088929.png", record_pos=(0.418, -0.188), resolution=(1280, 720))):
        find_click(Template(r"img/tpl1646924779521.png", record_pos=(-0.001, 0.144), resolution=(1280, 720)))
    
    # 第一次领体力，第二次才全领完
    if last:
        find_click(
            Template(r"img/tpl1646924829347.png", record_pos=(-0.103, 0.239), resolution=(1280, 720)))
        find_click(Template(r"img/tpl1645873777133.png", record_pos=(-0.001, 0.145), resolution=(1280, 720)))

    # 返回主界面
    device().key_press("`")
    device().key_release("`")
    back_to_main()


# 一键减负
def sweep():
    # 打开材料活动界面
    back_to_main()
    find_click(Template(r"img/tpl1647269398565.png", record_pos=(0.358, -0.145), resolution=(1280, 720)))
    random_click(ax, ay, aw, ah)
    find_click(Template(r"img/tpl1645873106705.png", record_pos=(0.348, 0.119), resolution=(1280, 720)))

    # 材料活动一键减负
    find_click(Template(r"img/tpl1658801383239.png", record_pos=(0.411, 0.241), resolution=(1280, 720)))
    find_click(Template(r"img/tpl1645873249602.png", record_pos=(-0.001, 0.131), resolution=(1280, 720)))
    find_click(Template(r"img/tpl1645873276874.png", record_pos=(-0.001, 0.145), resolution=(1280, 720)))

    # 返回主界面
    for _ in range(2):
        device().key_press("`")
        device().key_release("`")
        sleep(1)
    back_to_main()


# 领凭证奖励
def bp():
    # 打开凭证界面
    back_to_main()
    find_click(Template(r"img/tpl1645871324073.png", record_pos=(-0.46, -0.186), resolution=(1280, 720)))
    random_click(100, 260, 180, 60)

    # 领每周箱子
    if datetime.today().weekday() == 0:
        find_click(Template(r"img/tpl1647269720839.png", record_pos=(0.334, 0.202), resolution=(1280, 720)))
        find_click(Template(r"img/tpl1646114916091.png", record_pos=(-0.136, 0.115), resolution=(1277, 720)), timeout=1)
        find_click(Template(r"img/tpl1645874627052.png", record_pos=(0.0, 0.144), resolution=(1280, 720)))
        if find_click(Template(r"img/tpl1646114953123.png", record_pos=(0.138, 0.219), resolution=(1277, 720)),
                      timeout=1):
            find_click(Template(r"img/tpl1646115009691.png", record_pos=(0.001, 0.145), resolution=(1277, 720)))

    # 领奖励
    random_click(px, py, pw, ph)
    if not find_click(Template(r"img/tpl1645875473026.png", record_pos=(0.14, 0.172), resolution=(1280, 720))):
        device().key_press("`")
        device().key_release("`")

    # 返回主界面
    sleep(1)
    device().key_press("`")
    device().key_release("`")
    back_to_main()


# 领邮件
def mail():
    # 打开邮件界面
    back_to_main()
    find_click(Template(r"img/tpl1646115129099.png", record_pos=(-0.427, -0.021), resolution=(1277, 720)))

    # 领邮件
    find_click(Template(r"img/tpl1646115235683.png", record_pos=(0.388, 0.246), resolution=(1277, 720)))
    find_click(Template(r"img/tpl1646115259631.png", record_pos=(0.0, 0.145), resolution=(1277, 720)))

    # 返回主界面
    device().key_press("`")
    device().key_release("`")
    back_to_main()


# 领舰团每周贡献奖励
def armada():
    # 打开舰团奖励界面
    back_to_main()
    find_click(Template(r"img/tpl1646115729748.png", record_pos=(0.191, 0.248), resolution=(1277, 720)))
    find_click(Template(r"img/tpl1646115760307.png", record_pos=(0.242, 0.242), resolution=(1277, 720)))

    # 领奖励
    find_click(Template(r"img/tpl1646115833659.png", record_pos=(-0.441, -0.123), resolution=(1277, 720)))
    find_click(Template(r"img/tpl1646116572972.png", record_pos=(0.0, 0.145), resolution=(1277, 720)))
    find_click(Template(r"img/tpl1646115855947.png", record_pos=(-0.44, -0.034), resolution=(1277, 720)))
    find_click(Template(r"img/tpl1646116572972.png", record_pos=(0.0, 0.145), resolution=(1277, 720)))
    find_click(Template(r"img/tpl1646115869755.png", record_pos=(-0.44, 0.055), resolution=(1277, 720)))
    find_click(Template(r"img/tpl1646116572972.png", record_pos=(0.0, 0.145), resolution=(1277, 720)))
    find_click(Template(r"img/tpl1646115888227.png", record_pos=(-0.44, 0.142), resolution=(1277, 720)))
    find_click(Template(r"img/tpl1646116572972.png", record_pos=(0.0, 0.145), resolution=(1277, 720)))
    find_click(Template(r"img/tpl1646115903419.png", record_pos=(-0.441, 0.23), resolution=(1277, 720)))
    find_click(Template(r"img/tpl1646116572972.png", record_pos=(0.0, 0.145), resolution=(1277, 720)))

    # 返回主界面
    for _ in range(2):
        device().key_press("`")
        device().key_release("`")
        sleep(1)
    back_to_main()
    

# 领吼姆秘宝
def homu_box():
    back_to_main()
    
    find_click(Template(r"img/tpl1658757306012.png", record_pos=(-0.428, 0.084), resolution=(1280, 720)))
    find_click(Template(r"img/tpl1658757346684.png", record_pos=(-0.409, -0.123), resolution=(1280, 720)))
    find_click(Template(r"img/tpl1658757375611.png", record_pos=(-0.409, -0.007), resolution=(1280, 720)))
    find_click(Template(r"img/tpl1658757404980.png", record_pos=(-0.206, 0.042), resolution=(1280, 720)))
    find_click(Template(r"img/tpl1658757433740.png", record_pos=(0.0, 0.18), resolution=(1280, 720)))
    find_click(Template(r"img/tpl1658757469148.png", record_pos=(-0.001, 0.145), resolution=(1280, 720)))
    
    back_to_main()


# 万象虚境肝锻造材料
# index: 虚境序号   ticket: 是否使用时序通行证
def xujing(index=3, ticket=True):
    back_to_main()
    find_click(Template(r"img/tpl1647269398565.png", record_pos=(0.358, -0.145), resolution=(1280, 720)))
    random_click(tx, ty, tw, th)
    find_click(Template(r"img/tpl1659094973381.png", record_pos=(0.14, 0.007), resolution=(1280, 720)))

    if index == 1:
        find_click(Template(r"img/tpl1659095822710.png", record_pos=(-0.349, 0.001), resolution=(1280, 720)))
    elif index == 2:
        find_click(Template(r"img/tpl1659095856742.png", record_pos=(-0.116, 0.001), resolution=(1280, 720)))
    elif index == 3:
        find_click(Template(r"img/tpl1659095893750.png", record_pos=(0.116, 0.001), resolution=(1280, 720)))
    else:
        find_click(Template(r"img/tpl1659095915789.png", record_pos=(0.349, 0.001), resolution=(1280, 720)))
    # 选第2关
    p1 = random_coordinate(400, 200, 450, 100)
    p2 = random_coordinate(400, 800, 450, 100)
    swipe(p1, p2)
    random_click(sx, sy, sw, sh)

    # 进入战斗
    if datetime.today().weekday() in [4, 5, 6]:
        repeat = 2
    else:
        repeat = 1
    for _ in range(repeat):
        find_click(Template(r"img/tpl1659098326087.png", record_pos=(0.373, 0.245), resolution=(1280, 720)))
        find_click(Template(r"img/tpl1659098496079.png", record_pos=(0.363, 0.245), resolution=(1280, 720)))
        find_click(Template(r"img/tpl1659098774047.png", record_pos=(0.373, 0.237), resolution=(1280, 720)))
        sleep(5)
        combo()
        while exists(Template(r"img/tpl1659103297418.png", record_pos=(-0.46, -0.256), resolution=(1280, 720))):
            action()

        sleep(random.randint(6, 9))
        random_click(365, 365, 500, 500)
        if ticket:
            find_click(Template(r"img/tpl1659103179194.png", record_pos=(0.154, 0.204), resolution=(1280, 720)))
        else:
            find_click(Template(r"img/tpl1659103757994.png", record_pos=(-0.154, 0.205), resolution=(1280, 720)))
        find_click(Template(r"img/tpl1659103209330.png", record_pos=(-0.001, 0.144), resolution=(1280, 720)))
        
    for _ in range(3):
        sleep(1)
        device().key_press("`")
        device().key_release("`")
    back_to_main()
