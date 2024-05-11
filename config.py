import json
from pathlib import Path
from typing import Literal, List, Union, Optional

from pydantic import BaseModel, Field


class Argument(BaseModel):
    """
    Minimum setting
    """
    type: Literal['input', 'select', 'checkbox'] = 'input'
    value: Union[str, bool]
    option: List[str] = []
    hide: bool = False


class GCustomBase(BaseModel):
    """
    Basic settings for every task
    """
    priority: Optional[int] = 3
    priority_enabled: Optional[bool] = True
    command: Optional[str] = ''
    command_enabled: Optional[bool] = True


class GGeneralBase(BaseModel):
    """
    General settings for the project
    """
    work_dir: Optional[str] = './examples/HonkaiHelper'
    work_dir_enabled: Optional[bool] = True
    is_background: Optional[bool] = False
    is_background_enabled: Optional[bool] = True
    config_path: Optional[str] = './examples/HonkaiHelper/config/config.json'
    config_path_enabled: Optional[bool] = True


# 以下是实际设置内容
# 任务级别
class TGeneral(BaseModel):
    class GGame(BaseModel):
        game_path: Argument = Argument(type='input', value='')
        log_retain: Argument = Argument(type='select', value='1week', option=['1day', '3days', '1week', '1month'])

    Base: GGeneralBase = Field(GGeneralBase(), alias='_Base')
    Game: GGame = GGame()


class TArmada(BaseModel):
    Base: GCustomBase = Field(GCustomBase(command='./examples/HonkaiHelper/tools/python/python.exe main.py -t armada',
                                          priority=5), alias='_Base')


class TDormBonus(BaseModel):
    Base: GCustomBase = Field(GCustomBase(command='./examples/HonkaiHelper/tools/python/python.exe main.py -t dorm_bonus',
                                          priority=2), alias='_Base')


class TErrand(BaseModel):
    Base: GCustomBase = Field(GCustomBase(command='./examples/HonkaiHelper/tools/python/python.exe main.py -t errand',
                                          priority=3), alias='_Base')


class TExpedition(BaseModel):
    Base: GCustomBase = Field(GCustomBase(command='./examples/HonkaiHelper/tools/python/python.exe main.py -t expedition',
                                          priority=4), alias='_Base')


class TLogin(BaseModel):
    Base: GCustomBase = Field(GCustomBase(command='./examples/HonkaiHelper/tools/python/python.exe main.py -t login',
                                          priority=0, priority_enabled=False), alias='_Base')


class TLogout(BaseModel):
    Base: GCustomBase = Field(GCustomBase(command='./examples/HonkaiHelper/tools/python/python.exe main.py -t logout',
                                          priority=100, priority_enabled=False), alias='_Base')


class TMail(BaseModel):
    Base: GCustomBase = Field(GCustomBase(command='./examples/HonkaiHelper/tools/python/python.exe main.py -t mail',
                                          priority=7), alias='_Base')


class TMission1(BaseModel):
    Base: GCustomBase = Field(GCustomBase(command='./examples/HonkaiHelper/tools/python/python.exe main.py -t mission',
                                          priority=1, priority_enabled=False), alias='_Base')


class TMission2(BaseModel):
    Base: GCustomBase = Field(GCustomBase(command='./examples/HonkaiHelper/tools/python/python.exe main.py -t mission',
                                          priority=99, priority_enabled=False), alias='_Base')


class TSweep(BaseModel):
    Base: GCustomBase = Field(GCustomBase(command='./examples/HonkaiHelper/tools/python/python.exe main.py -t sweep',
                                          priority=6), alias='_Base')


# 任务组级别
class MProject(BaseModel):
    General: TGeneral = TGeneral()


class MDaily(BaseModel):
    Login: TLogin = TLogin()
    Logout: TLogout = TLogout()
    Mission1: TMission1 = TMission1()
    Mission2: TMission2 = TMission2()
    Sweep: TSweep = TSweep()
    Mail: TMail = TMail()
    DormBonus: TDormBonus = TDormBonus()
    Expedition: TExpedition = TExpedition()
    Errand: TErrand = TErrand()
    Armada: TArmada = TArmada()


# 项目级别
class Config(BaseModel):
    Project: MProject = MProject()
    Daily: MDaily = MDaily()


def gen_i18n(config: BaseModel, lang: str):
    trans_dict = {
        "Menu": {},
        "Task": {},
    }

    # Check if the file already exists
    file_path = f'./config/i18n/{lang}.json'
    if Path(file_path).exists():
        # Load the existing translations
        with open(file_path, 'r', encoding='utf-8') as f:
            old_trans_dict = json.load(f)
    else:
        old_trans_dict = {}

    for menu, tasks in config.model_dump(by_alias=True).items():
        trans_dict['Menu'][menu] = old_trans_dict.get('Menu', {}).get(menu, {'name': ''})

        for task, groups in tasks.items():
            trans_dict['Task'][task] = old_trans_dict.get('Task', {}).get(task, {'name': ''})

            for group, args in groups.items():
                if group == '_Base':
                    continue
                if group not in trans_dict:
                    trans_dict[group] = {}

                trans_dict[group]['_info'] = old_trans_dict.get(group, {}).get('_info', {'name': '', 'help': ''})
                for arg, info in args.items():
                    trans_dict[group][arg] = old_trans_dict.get(group, {}).get(arg, {'name': '', 'help': ''})
                    if info['type'] == 'select':
                        for option in info['option']:
                            trans_dict[group][arg][option] = old_trans_dict.get(group, {}).get(arg, {}).get(option, '')

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(trans_dict, f, ensure_ascii=False, indent=2)


def export():
    config = Config()
    with open('config/args.json', 'w') as f:
        f.write(config.model_dump_json(indent=2, by_alias=True))

    gen_i18n(config, 'zh_CN')


if __name__ == '__main__':
    export()
