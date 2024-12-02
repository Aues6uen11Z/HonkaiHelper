from zafkiel import Template, logger, Timer, find_click, exists
from zafkiel.exception import LoopError
from zafkiel.ocr import Keyword
from zafkiel.ui import UI

from config import Config
from tasks.base.page import page_battle, page_lite, TPL_CONFIRM_BUTTON
from tasks.base.switch import TPL_BATTLE_ATTACK_TAB


class Sweep(UI):
    def __init__(self, config: Config = None):
        self.config = config

    def run(self):
        self.ui_ensure(page_battle, TPL_BATTLE_ATTACK_TAB)
        self.ui_goto(page_lite)

        if not exists(Template(r"QUICK_LITE.png", (0.41, 0.241), Keyword('一键减负'))):
            logger.info('Material sweep already completed')
            return

        loop_timer = Timer(0, 10).start()
        while True:
            if loop_timer.reached():
                raise LoopError('The operation has looped too many times')

            find_click(Template(r"QUICK_LITE.png", (0.41, 0.241), Keyword('一键减负')))
            find_click(Template(r"LITE_BUTTON.png", (0.0, 0.133), Keyword('减负')))
            if find_click(TPL_CONFIRM_BUTTON):
                logger.info('Material sweep completed')
                break

