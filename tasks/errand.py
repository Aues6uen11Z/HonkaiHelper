from typing import Dict

from zafkiel import Template, logger, Timer
from zafkiel.exception import LoopError
from zafkiel.ocr import Ocr, DigitCounter, Keyword
from zafkiel.ui import UI
from zafkiel.utils import crop, color_exists

from tasks.base.page import page_errands, TPL_RETURN_BUTTON, TPL_CONFIRM_BUTTON


class Errand(UI):
    def __init__(self, config: Dict = None):
        self.config = config

    def dispatch(self):
        loop_timer = Timer(0, 10).start()
        while True:
            if loop_timer.reached():
                raise LoopError('The operation has looped too many times')

            self.find_click(Template(r"QUICK_ERRAND.png", (0.283, 0.251), Keyword('一键打工')))
            if self.find_click(Template(r"QUICK_ERRAND_CONFIRM.png", (0.141, 0.204), Keyword('一键打工'), rgb=True),
                               times=2):
                logger.info('Errand dispatch completed')
                break
            if self.exists(Template(r"ERRAND_DISABLE.png", (0.141, 0.203), rgb=True)):
                self.find_click(Template(r"ERRAND_CANCEL.png", (-0.141, 0.204), Keyword('取消')))
                logger.info('No place available for dispatch')
                break

    def claim_rewards(self):
        loop_timer = Timer(0, 10).start()
        while True:
            if self.exists(Template(r"ERRAND_REWARD_DONE.png", (0.42, 0.249), rgb=True)):
                logger.info('Errand rewards claim completed')
                break

            if loop_timer.reached():
                raise LoopError('The operation has looped too many times')

            self.find_click(Template(r"ERRAND_REWARD_CLAIM.png", (0.419, 0.25), Keyword('领取奖励'), rgb=True))
            self.find_click(TPL_CONFIRM_BUTTON)

    def run(self):
        self.ui_ensure(page_errands)
        self.claim_rewards()
        self.dispatch()
