# -*- encoding=utf8 -*-

from airtest.core.api import *
from airtest.cli.parser import cli_setup

if not cli_setup():
    auto_setup(__file__, logdir=True, devices=["Windows:///?title=崩坏3", ])

# 登录前有可能要更新数据
def check_update():
    pass

# 刚上线的一系列操作
def login():
    wait(Template(r"tpl1645517341582.png", record_pos=(-0.015, 0.131), resolution=(1280, 720)), timeout=120, interval=3,
         intervalfunc=check_update)
