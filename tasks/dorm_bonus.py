from zafkiel import Template, logger, find_click, screenshot
from zafkiel.ocr import Digit
from zafkiel.ui import UI

from config import Config
from tasks.base.page import page_dorm


class DormBonus(UI):
    def __init__(self, config: Config = None):
        self.config = config

    def claim_stamina(self):
        logger.info('Start claiming dorm stamina')
        self.ui_ensure(page_dorm)
        if find_click(Template(r"DORM_STAMINA.png", (-0.34, -0.059))):
            # 取存储的体力
            ocr = Digit(Template(r"DORM_STAMINA_SURPLUS.png", (-0.025, 0.077)))
            if ocr.ocr_single_line(screenshot()) > 0:
                find_click(Template(r"CLAIM_STAMINA.png", (0.092, 0.156)), times=2)
                logger.info('Dorm stamina claim completed')
                return
        find_click(Template(r"DORM_STAMINA_CLOSE.png", (0.349, -0.181)))

    def claim_gold(self):
        logger.info('Start claiming dorm gold')
        self.ui_ensure(page_dorm)
        if find_click(Template(r"DORM_GOLD.png", (-0.216, -0.071)), times=2):
            logger.info('Dorm gold claim completed')

    def run(self):
        self.claim_gold()
        self.claim_stamina()
