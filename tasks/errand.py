from zafkiel import Template, logger
from zafkiel.ocr import Ocr, DigitCounter, Keyword
from zafkiel.ui import UI
from zafkiel.utils import crop, color_exists

from tasks.base.page import page_errands, TPL_RETURN_BUTTON, TPL_CONFIRM_BUTTON


class Errand(UI):
    # 打工派遣
    def dispatch(self):
        ocr = Ocr(Template(r"ERRAND_LIST.png", (0.427, 0.005)))
        digit_ocr = DigitCounter(Template(r"ERRAND_ONIGIRI.png", (-0.037, 0.245)))
        TPL_ERRAND_QUALITY = Template(r"ERRAND_QUALITY.png", (-0.305, 0.03))
        target_idx = 0  # 选第几个打工，由于我的号没不符合条件的情况，所以这个功能没测试

        while True:
            screen = self.screenshot()
            enter_button = None

            try:
                enter_button = ocr.ocr_match_keyword(screen, Keyword('需要'), mode=1)[target_idx].area
            except IndexError:
                boxed_results = ocr.detect_and_ocr(screen)
                if len(boxed_results) < 5:  # 列表没加载完全
                    continue
                elif ocr.ocr_match_keyword(screen, Keyword('剩余'), mode=1):  # 没有可派遣的打工
                    logger.info('完成打工派遣')
                    break

            self.touch(enter_button)
            self.find_click(Template(r"ERRAND_DISPATCH.png", (0.18, 0.246)))

            # 检查打工需要的特性是否满足
            screen = self.screenshot()
            quality_check = crop(screen, TPL_ERRAND_QUALITY.area)
            if color_exists(quality_check, (255, 94, 65)):
                target_idx += 1
                continue

            # 检查饭团是否足够
            if digit_ocr.ocr_single_line(screen)[1] < 0:
                self.find_click(TPL_RETURN_BUTTON)
                logger.info('完成打工派遣')
                break

            self.find_click(Template(r"ERRAND_START.png", (0.388, 0.245)))

    # 领前一天打工奖励
    def claim_rewards(self):
        self.find_click(Template(r"GET_ERRAND_LIST.png", (0.48, -0.001)), timeout=0)
        while self.find_click(Template(r"ERRAND_COMPLETE.png", (0.38, -0.248), Keyword('完成'))):
            self.find_click(TPL_CONFIRM_BUTTON)
        logger.info('领取打工奖励')

    def run(self):
        self.ui_ensure(page_errands)
        self.claim_rewards()
        self.dispatch()
