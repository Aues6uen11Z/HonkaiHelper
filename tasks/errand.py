from typing import Dict

from zafkiel import Template, logger, Timer
from zafkiel.exception import ScriptError
from zafkiel.ocr import Ocr, DigitCounter, Keyword
from zafkiel.ui import UI
from zafkiel.utils import crop, color_exists

from tasks.base.page import page_errands, TPL_RETURN_BUTTON, TPL_CONFIRM_BUTTON


class Errand(UI):
    def __init__(self, config: Dict = None):
        self.config = config

    # 打工派遣
    def dispatch(self):
        ocr = Ocr(Template(r"ERRAND_LIST.png", (0.427, 0.005)))
        digit_ocr = DigitCounter(Template(r"ERRAND_ONIGIRI.png", (-0.037, 0.245)))
        TPL_ERRAND_QUALITY = Template(r"ERRAND_QUALITY.png", (-0.305, 0.03))
        target_idx = 0  # 选第几个打工，由于我的号没不符合条件的情况，所以这个功能没测试

        loop_timer = Timer(0, 20).start()
        confirm_timer = Timer(3)
        while True:
            if loop_timer.reached():
                raise ScriptError('The operation has looped too many times')

            screen = self.screenshot()
            enter_button = None
            try:
                enter_button = ocr.ocr_match_keyword(screen, Keyword('需要'), mode=1)[target_idx].area
            except IndexError:
                boxed_results = ocr.detect_and_ocr(screen)
                if len(boxed_results) < 5:  # 列表没加载完全
                    continue
                elif ocr.ocr_match_keyword(screen, Keyword('剩余'), mode=1):  # 没有可派遣的打工
                    logger.info('Errand dispatch completed')
                    break
            if enter_button:
                enter_button = (enter_button[0]+enter_button[2])/2, (enter_button[1]+enter_button[3])/2
                self.touch(enter_button, v_name='ERRAND_LIST')

            self.find_click(Template(r"ERRAND_DISPATCH.png", (0.18, 0.246), Keyword('一键派遣')))

            # 检查打工需要的特性是否满足
            screen = self.screenshot()
            quality_check = crop(screen, TPL_ERRAND_QUALITY.area)
            if color_exists(quality_check, (255, 94, 65)):
                # logger.info()
                target_idx += 1
                continue

            # 检查饭团是否足够
            if digit_ocr.ocr_single_line(screen)[1] < 0:
                self.find_click(TPL_RETURN_BUTTON)
                logger.info('Errand dispatch completed')
                break

            # 确保跳出界面
            confirm_timer.reset()
            while self.find_click(Template(r"ERRAND_START.png", (0.388, 0.245), Keyword('开始打工')), timeout=0):
                if confirm_timer.reached():
                    self.find_click(TPL_RETURN_BUTTON)
                    break
                self.sleep(0.5)

    # 领前一天打工奖励
    def claim_rewards(self):
        self.find_click(Template(r"GET_ERRAND_LIST.png", (0.48, -0.001)), timeout=0)
        while self.find_click(Template(r"ERRAND_COMPLETE.png", (0.38, -0.248), Keyword('完成'))):
            self.find_click(TPL_CONFIRM_BUTTON)
        logger.info('Errand rewards claim completed')

    def run(self):
        self.ui_ensure(page_errands)
        self.claim_rewards()
        self.dispatch()

