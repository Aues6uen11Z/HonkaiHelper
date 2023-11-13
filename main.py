import ctypes
import os
import shutil
import sys

from zafkiel import API, simple_report

import config
from tasks.armada import Armada
from tasks.dorm_bonus import DormBonus
from tasks.errand import Errand
from tasks.expedition import Expeditions
from tasks.login import Login
from tasks.mission import Missions
from tasks.sweep import Sweep


def main():
    # 清除上一次的报告
    if os.path.exists('log'):
        shutil.rmtree('log')

    # 日常
    Login().app_start()
    Missions().run()
    DormBonus().claim_stamina()
    DormBonus().claim_gold()
    Errand().run()
    Expeditions().run()
    Armada().run()
    Sweep().run()
    Missions().run()

    # 结束游戏进程
    API().stop_app()

    # 生成报告
    simple_report(__file__, output='log/log.html')


if __name__ == '__main__':
    # 以管理员身份运行
    if ctypes.windll.shell32.IsUserAnAdmin():
        main()
    else:
        ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable, __file__, None, 1)
