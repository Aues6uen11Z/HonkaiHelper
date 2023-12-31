from zafkiel import Template
from zafkiel.ocr import Keyword
from zafkiel.ui import Page

from tasks.base.switch import switch_missions, switch_expeditions, TPL_GOTO_ATTACK, switch_battle

TPL_RETURN_BUTTON = Template(r"RETURN_BUTTON.png", (-0.444, -0.256), Keyword('返回'))
TPL_HOME_BUTTON = Template(r"HOME_BUTTON.png", (-0.298, -0.257), Keyword('主菜单'))
TPL_CONFIRM_BUTTON = Template(r"CONFIRM_BUTTON.png", (0.0, 0.144), Keyword('确定'))

# 主界面
page_main = Page(Template(r"MAIN_FLAG.png", (0.281, 0.043), rgb=True))

# 家园界面
page_dorm = Page(Template(r"DORM_STAMINA.png", (-0.34, -0.059)))
page_dorm.link(TPL_RETURN_BUTTON,
               destination=page_main)
page_main.link(Template(r"MAIN_GOTO_DORM.png", (0.354, 0.244), Keyword('家园')),
               destination=page_dorm)

# 舰团界面
page_armada = Page(Template(r"ARMADA_FLAG.png", (0.113, 0.076)))
page_armada.link(TPL_RETURN_BUTTON,
                 destination=page_main)
page_main.link(Template(r"MAIN_GOTO_ARMADA.png", (0.195, 0.244), Keyword('舰团')),
               destination=page_armada)

# 舰团委托界面
page_commission = Page(Template(r"COMMISSION_FLAG.png", (-0.392, -0.183), Keyword('回收委托')))
page_commission.link(TPL_RETURN_BUTTON,
                     destination=page_armada)
page_commission.link(TPL_HOME_BUTTON,
                     destination=page_main)
page_armada.link(Template(r"ARMADA_GOTO_COMMISSION.png", (-0.113, 0.227), Keyword('委托回收')),
                 destination=page_commission)

# 舰团奖池界面
page_armada_rewards = Page(Template(r"ARMADA_REWARD_FLAG.png", (-0.394, -0.184), Keyword('舰团奖池')))
page_armada_rewards.link(TPL_RETURN_BUTTON,
                         destination=page_armada)
page_armada_rewards.link(TPL_HOME_BUTTON,
                         destination=page_main)
page_commission.link(Template(r"COMMISSION_GOTO_REWARD.png", (0.439, -0.104), Keyword('舰团奖池')),
                     destination=page_armada_rewards)

# BP任务界面
page_missions = Page(Template(r"GOTO_BP_MISSIONS.png", (-0.417, -0.171), Keyword('作战任务')),
                     switch=switch_missions)
page_missions.link(TPL_RETURN_BUTTON,
                   destination=page_main)
page_main.link(Template(r"MAIN_GOTO_MISSIONS.png", (-0.454, -0.201)),
               destination=page_missions)

# 邮件界面
page_mail = Page(Template(r"MAIL_FLAG.png", (-0.456, 0.23), Keyword('邮件数')))
page_mail.link(TPL_RETURN_BUTTON,
               destination=page_main)
page_main.link(Template(r"MAIN_GOTO_MAIL.png", (-0.42, -0.039)),
               destination=page_mail)

# 远征界面
page_expeditions = Page(Template(r"EXPEDITION_FLAG.png", (-0.363, -0.183), Keyword('今日远征可用体力')),
                        switch=switch_expeditions)
page_expeditions.link(TPL_RETURN_BUTTON,
                      destination=page_dorm)
page_expeditions.link(TPL_HOME_BUTTON,
                      destination=page_main)
page_dorm.link(Template(r"DORM_GOTO_EXPEDITIONS.png", (0.155, 0.237), Keyword('远征')),
               destination=page_expeditions)

# 远征派遣界面
page_dispatch = Page(Template(r"QUICK_DISPATCH.png", (0.119, 0.227), Keyword('一键派遣')))
page_dispatch.link(TPL_RETURN_BUTTON,
                   destination=page_expeditions)
page_dispatch.link(TPL_HOME_BUTTON,
                   destination=page_main)

# 打工界面
page_errands = Page(Template(r"ERRANDS_FLAG.png", (-0.077, -0.258), rgb=True))
page_errands.link(TPL_RETURN_BUTTON,
                  destination=page_dorm)
page_dorm.link(Template(r"DORM_GOTO_ERRANDS.png", (0.277, 0.235), Keyword('打工')),
               destination=page_errands)

# 商店界面
page_shop = Page(Template(r"SHOP_FLAG.png", (-0.474, -0.191)))
page_shop.link(TPL_RETURN_BUTTON,
               destination=page_dorm)
page_shop.link(TPL_HOME_BUTTON,
               destination=page_main)
page_dorm.link(Template(r"DORM_GOTO_SHOP.png", (0.422, 0.237), Keyword('商店')),
               destination=page_shop)

# 出击界面
page_battle = Page(TPL_GOTO_ATTACK,
                   switch=switch_battle)
page_battle.link(Template(r"NEW_HOME_BUTTON.png", (-0.343, -0.252)),
                 destination=page_main)
page_main.link(Template(r"MAIN_GOTO_BATTLE.png", (0.421, -0.004), Keyword('出击')),
               destination=page_battle)

# 材料活动界面
page_lite = Page(Template(r"LITE_FLAG.png", (-0.043, -0.087)))
page_lite.link(TPL_RETURN_BUTTON,
               destination=page_battle)
page_lite.link(TPL_HOME_BUTTON,
               destination=page_main)
page_battle.link(Template(r"BATTLE_GOTO_LITE.png", (-0.314, 0.147)),
                 destination=page_lite)
