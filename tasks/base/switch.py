from zafkiel import Template
from zafkiel.ocr import Keyword
from zafkiel.ui import Switch

# BP任务界面
TPL_BP_MISSIONS_TAB = Template(r"BP_MISSIONS_TAB.png", (0.449, 0.24))
TPL_BP_REWARDS_TAB = Template(r"BP_REWARDS_TAB.png", (-0.273, -0.044))
TPL_GOTO_BP_MISSIONS = Template(r"GOTO_BP_MISSIONS.png", (-0.417, -0.171), Keyword('作战任务'))
TPL_GOTO_BP_REWARDS = Template(r"GOTO_BP_REWARDS.png", (-0.42, -0.102), Keyword('作战奖励'))

switch_missions = Switch('switch_missions', is_selector=True)
switch_missions.add_state('BP_MISSIONS_TAB', TPL_BP_MISSIONS_TAB, TPL_GOTO_BP_MISSIONS)
switch_missions.add_state('BP_REWARDS_TAB', TPL_BP_REWARDS_TAB, TPL_GOTO_BP_REWARDS)


# 远征界面
TPL_EXPEDITION_FRAG_TAB = Template(r"EXPEDITION_FRAG_TAB.png", (0.369, -0.196), rgb=True)
TPL_EXPEDITION_MATL_TAB = Template(r"EXPEDITION_MATL_TAB.png", (0.37, -0.135), rgb=True)
TPL_MATL_GOTO_FRAG = Template(r"MATL_GOTO_FRAG.png", (0.369, -0.197), rgb=True)
TPL_FRAG_GOTO_MATL = Template(r"FRAG_GOTO_MATL.png", (0.369, -0.136), rgb=True)

switch_expeditions = Switch('switch_expeditions', is_selector=True)
switch_expeditions.add_state('EXPEDITION_FRAG_TAB', TPL_EXPEDITION_FRAG_TAB, TPL_MATL_GOTO_FRAG)
switch_expeditions.add_state('EXPEDITION_MATL_TAB', TPL_EXPEDITION_MATL_TAB, TPL_FRAG_GOTO_MATL)


# 作战界面
TPL_BATTLE_RECOMMEND_TAB = Template(r"BATTLE_RECOMMEND_TAB.png", (0.005, 0.148))
TPL_BATTLE_ATTACK_TAB = Template(r"BATTLE_ATTACK_TAB.png", (-0.047, 0.152))
TPL_BATTLE_CHALLENGE_TAB = Template(r"BATTLE_CHALLENGE_TAB.png", (0.228, -0.077))
TPL_BATTLE_EVENT_TAB = Template(r"BATTLE_EVENT_TAB.png", (-0.349, -0.114))
TPL_GOTO_RECOMMEND = Template(r"GOTO_RECOMMEND.png", (-0.183, -0.202), Keyword('推荐'))
TPL_GOTO_ATTACK = Template(r"GOTO_ATTACK.png", (-0.072, -0.202), Keyword('出击'))
TPL_GOTO_CHALLENGE = Template(r"GOTO_CHALLENGE.png", (0.066, -0.202), Keyword('挑战'))
TPL_GOTO_EVENT = Template(r"GOTO_EVENT.png", (0.199, -0.202), Keyword('活动'))

switch_battle = Switch('switch_battle', is_selector=True)
switch_battle.add_state('BATTLE_RECOMMEND_TAB', TPL_BATTLE_RECOMMEND_TAB, TPL_GOTO_RECOMMEND)
switch_battle.add_state('BATTLE_ATTACK_TAB', TPL_BATTLE_ATTACK_TAB, TPL_GOTO_ATTACK)
switch_battle.add_state('BATTLE_CHALLENGE_TAB', TPL_BATTLE_CHALLENGE_TAB, TPL_GOTO_CHALLENGE)
switch_battle.add_state('BATTLE_EVENT_TAB', TPL_BATTLE_EVENT_TAB, TPL_GOTO_EVENT)
