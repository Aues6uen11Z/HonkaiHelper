from zafkiel import Template, Timer, logger, find_click, exists
from zafkiel.exception import LoopError
from zafkiel.ocr import Ocr, Keyword
from zafkiel.ui import UI

from config import Config
from tasks.base.page import page_expeditions, TPL_CONFIRM_BUTTON
from tasks.base.switch import TPL_EXPEDITION_MATL_TAB, TPL_EXPEDITION_FRAG_TAB


class Expeditions(UI):
    def __init__(self, config: Config = None):
        self.config = config

    # 远征派遣
    @staticmethod
    def dispatch():
        loop_timer = Timer(0, 10).start()
        while True:
            if loop_timer.reached():
                raise LoopError('The operation has looped too many times')

            find_click(Template(r"QUICK_EXPEDITION.png", (0.409, 0.237), Keyword('一键远征')))
            if exists(Template(r"EXPEDITION_NOT_AVAILABLE.png", (0.209, -0.045), Keyword('次数不足')), ocr_mode=1):
                find_click(Template(r"EXPEDITION_CANCEL.png", (-0.141, 0.205), Keyword('取消派遣')))
                break
            if find_click(Template(r"EXPEDITION_DISPATCH.png", (0.14, 0.205), Keyword('远征派遣')), times=2):
                if find_click(Template(r"CLAIM_STAMINA.png", (0.092, 0.156), Keyword('取出体力')), times=2):
                    find_click(Template(r"EXPEDITION_DISPATCH.png", (0.14, 0.205), Keyword('远征派遣')), times=2)
                logger.info('Expedition dispatch completed')
                break

    # 领前一天远征奖励 TODO: 记录远征类型
    def claim_rewards(self):
        TPL_EXPEDITION_COMPLETED = Template(r"EXPEDITION_COMPLETED.png", (0.237, -0.09), Keyword('完成远征'))
        if not exists(TPL_EXPEDITION_COMPLETED, timeout=1):
            current_state = self.ui_get_current_state(self.ui_get_current_page().switch)
            another_state = TPL_EXPEDITION_MATL_TAB if current_state == TPL_EXPEDITION_FRAG_TAB.name \
                else TPL_EXPEDITION_FRAG_TAB
            self.ui_goto(page_expeditions, another_state)
        if find_click(TPL_EXPEDITION_COMPLETED):
            find_click(TPL_CONFIRM_BUTTON)
            logger.info('Expedition rewards claim completed')

    def run(self):
        self.ui_ensure(page_expeditions)
        self.claim_rewards()
        self.dispatch()
