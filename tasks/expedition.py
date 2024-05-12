from typing import Dict

from zafkiel import Template, Timer, logger
from zafkiel.exception import LoopError
from zafkiel.ocr import Ocr, Keyword
from zafkiel.ui import UI

from tasks.base.page import page_expeditions, TPL_RETURN_BUTTON, TPL_CONFIRM_BUTTON
from tasks.base.switch import TPL_EXPEDITION_MATL_TAB, TPL_EXPEDITION_FRAG_TAB


class Expeditions(UI):
    def __init__(self, config: Dict = None):
        self.config = config

    # 远征派遣
    # TODO: 远征类型写进配置
    def dispatch(self):
        ocr_dispatch = Ocr(Template(r"START_EXPEDITION.png", (0.239, 0.057), Keyword('开始远征')))
        ocr_fail = Ocr(Template(r"DISPATCH_FAIL.png", (0.207, -0.004), Keyword('派遣')))

        miss_count = Timer(3, 5).start()  # 防止没识别到“无法派遣”黑条进入死循环
        loop_timer = Timer(0, 20).start()
        while True:
            if loop_timer.reached():
                raise LoopError('The operation has looped too many times')

            screen = self.screenshot()
            start_button = None
            try:
                if not miss_count.reached():
                    start_button = ocr_dispatch.ocr_match_keyword(screen, ocr_dispatch.button.keyword)[0].area
            except IndexError:
                boxed_results = ocr_dispatch.detect_and_ocr(screen)
                if len(boxed_results) < 8:  # 列表没加载完全
                    continue
                else:  # 这一页没有可派遣的远征
                    self.swipe(Template(r"SWIPE_START.png", (0.238, 0.207), rgb=True),
                               Template(r"SWIPE_END.png", (0.281, -0.184)), blind1=True)
                    continue

            miss_count.reset()
            if start_button:
                start_button = (start_button[0] + start_button[2]) / 2, (start_button[1] + start_button[3]) / 2
                self.touch(start_button, v_name='START_EXPEDITION')
            self.find_click(Template(r"QUICK_DISPATCH.png", (0.119, 0.227), Keyword('一键派遣')))
            self.find_click(Template(r"DISPATCH_CONFIRM.png", (0.362, 0.227), Keyword('确定探险')))
            self.sleep(0.3)
            if ocr_fail.ocr_match_keyword(self.screenshot(), ocr_fail.button.keyword, mode=1):
                self.find_click(TPL_RETURN_BUTTON, times=2)
                logger.info('Expedition dispatch completed')
                break

    # 领前一天远征奖励
    def claim_rewards(self):
        TPL_EXPEDITION_COMPLETED = Template(r"EXPEDITION_COMPLETED.png", (0.237, -0.09), Keyword('完成远征'))
        if not self.exists(TPL_EXPEDITION_COMPLETED, timeout=1):
            current_state = self.ui_get_current_state(self.ui_get_current_page().switch)
            another_state = TPL_EXPEDITION_MATL_TAB if current_state == TPL_EXPEDITION_FRAG_TAB.name \
                else TPL_EXPEDITION_FRAG_TAB
            self.ui_goto(page_expeditions, another_state)
        if self.find_click(TPL_EXPEDITION_COMPLETED):
            self.find_click(TPL_CONFIRM_BUTTON)
            logger.info('Expedition rewards claim completed')

    def run(self):
        self.ui_ensure(page_expeditions)
        self.claim_rewards()
        self.dispatch()
