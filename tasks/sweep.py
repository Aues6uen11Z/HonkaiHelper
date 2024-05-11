from typing import Dict

from zafkiel import Template, logger, Timer
from zafkiel.exception import ScriptError
from zafkiel.ocr import Keyword
from zafkiel.ui import UI

from tasks.base.page import page_battle, page_lite, TPL_CONFIRM_BUTTON
from tasks.base.switch import TPL_BATTLE_ATTACK_TAB


class Sweep(UI):
    def __init__(self, config: Dict = None):
        self.config = config

    def run(self):
        self.ui_ensure(page_battle, TPL_BATTLE_ATTACK_TAB)
        self.ui_goto(page_lite)

        TPL_QUICK_LITE = Template(r"QUICK_LITE.png", (0.41, 0.241), Keyword('一键减负'))
        loop_timer = Timer(0, 10).start()
        while True:
            if loop_timer.reached():
                raise ScriptError('The operation has looped too many times')

            if not self.exists(TPL_QUICK_LITE):
                logger.info('Material sweep already done')
                break

            if self.find_click(TPL_CONFIRM_BUTTON):
                logger.info('Material sweep completed')
                break
            if self.find_click(Template(r"LITE_BUTTON.png", (0.0, 0.133), Keyword('减负')), timeout=0):
                continue
            if self.find_click(TPL_QUICK_LITE, timeout=0):
                continue
