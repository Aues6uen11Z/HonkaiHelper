# -*- encoding=utf8 -*-

import os

from airtest.core.api import *
from airtest.cli.parser import cli_setup

from config import *

os.system(game_path)

if not cli_setup():
    auto_setup(__file__, logdir=True, devices=["Windows:///?title=崩坏3", ])


# script content
print("start...")
# generate html report
# from airtest.report.report import simple_report
# simple_report(__file__, logpath=True)

print(1)
