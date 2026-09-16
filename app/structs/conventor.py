
from typing import Any, TypeVar
from copy import deepcopy
from ctypes import Structure

from .steam import *
from .xbox import *
from .mobile import *
import app.utils as utils

T = TypeVar('T')
def _copy_attr(from_: object, to: T, ignore_incompatible_types: bool = True) -> T:
    assert isinstance(to, Structure)
    assert isinstance(from_, Structure)
    for field in from_._fields_:
        field_name = field[0]
        field_value = getattr(from_, field_name)
        try:
            setattr(to, field_name, field_value)
        except TypeError:
            if not ignore_incompatible_types:
                raise
    return to

def steam2xbox(data: PresideData) -> PresideDataXbox:
    """
    将 Steam 存档数据转换为 Xbox 存档数据。
    """
    xbox = PresideDataXbox.new()
    
    # OptionWorkXbox
    option_work_steam = data.system_data_.option_work_
    option_work_xbox = OptionWorkXbox.new()
    _copy_attr(option_work_steam, option_work_xbox)
    # SystemDataXbox
    system_data_steam = data.system_data_
    system_data_xbox = SystemDataXbox.new()
    _copy_attr(system_data_steam, system_data_xbox)
    system_data_xbox.option_work_ = option_work_xbox
    xbox.system_data_ = system_data_xbox
    
    # GameDataXbox
    for i, game_data_steam in enumerate(data.slot_list_):
        msg_data_steam = game_data_steam.msg_data_
        msg_data_xbox = MessageDataXbox.new()
        _copy_attr(msg_data_steam, msg_data_xbox)
        
        game_data_xbox = GameDataXbox.new()
        _copy_attr(game_data_steam, game_data_xbox)
        game_data_xbox.msg_data_ = msg_data_xbox
        xbox.slot_list_[i] = game_data_xbox
    
    return deepcopy(xbox)

def xbox2steam(data: PresideDataXbox) -> PresideData:
    """
    将 Xbox 存档数据转换为 Steam 存档数据。\n
    Xbox 存档中缺少的数据将会从默认空存档中读取。
    """
    steam = PresideData.new()
    default_save = PresideData.from_file(utils.abspath('res/steam_empty_save'))
    # OptionWork
    option_work_xbox = data.system_data_.option_work_
    option_work_steam = OptionWork.new()
    option_work_default = default_save.system_data_.option_work_
    _copy_attr(option_work_default, option_work_steam)
    _copy_attr(option_work_xbox, option_work_steam)
    # SystemData
    system_data_xbox = data.system_data_
    system_data_steam = SystemData.new()
    _copy_attr(system_data_xbox, system_data_steam)
    system_data_steam.option_work_ = option_work_steam
    steam.system_data_ = system_data_steam

    # GameData
    for i, game_data_xbox in enumerate(data.slot_list_):
        msg_data_xbox = game_data_xbox.msg_data_
        msg_data_steam = MessageData.new()
        msg_data_default = default_save.slot_list_[i].msg_data_
        _copy_attr(msg_data_default, msg_data_steam)
        _copy_attr(msg_data_xbox, msg_data_steam)

        game_data_steam = GameData.new()
        _copy_attr(game_data_xbox, game_data_steam)
        game_data_steam.msg_data_ = msg_data_steam
        steam.slot_list_[i] = game_data_steam

    return deepcopy(steam)

def xbox2mobile(data: PresideDataXbox) -> PresideDataMobile:
    """
    将 Xbox 存档数据转换为移动版（Android）存档数据。

    移动版与 Xbox 版的存档槽位数据（`GameData`）结构相同。
    """
    mobile = PresideDataMobile.new()
    mobile.save_version_ = Int32(1)
    # SystemDataMobile
    system_data_xbox = data.system_data_
    system_data_mobile = SystemDataMobile.new()
    _copy_attr(system_data_xbox, system_data_mobile)
    # OptionWorkMobile（字段类型不同，_copy_attr 会跳过整个 option_work_，需单独复制）
    option_work_mobile = OptionWorkMobile.new()
    _copy_attr(system_data_xbox.option_work_, option_work_mobile)
    system_data_mobile.option_work_ = option_work_mobile
    mobile.system_data_ = system_data_mobile

    # GameDataXbox（与移动版结构相同，可直接复制）
    for i, game_data_xbox in enumerate(data.slot_list_):
        mobile.slot_list_[i] = game_data_xbox

    mobile.expansion_data_.is_agree = bool_(1)
    return deepcopy(mobile)

def mobile2xbox(data: PresideDataMobile) -> PresideDataXbox:
    """
    将移动版（Android）存档数据转换为 Xbox 存档数据。
    """
    xbox = PresideDataXbox.new()
    # SystemDataXbox
    system_data_mobile = data.system_data_
    system_data_xbox = SystemDataXbox.new()
    _copy_attr(system_data_mobile, system_data_xbox)
    # OptionWorkXbox（字段类型不同，_copy_attr 会跳过整个 option_work_，需单独复制）
    option_work_xbox = OptionWorkXbox.new()
    _copy_attr(system_data_mobile.option_work_, option_work_xbox)
    system_data_xbox.option_work_ = option_work_xbox
    xbox.system_data_ = system_data_xbox

    # GameDataXbox（与移动版结构相同，可直接复制）
    for i, game_data_mobile in enumerate(data.slot_list_):
        xbox.slot_list_[i] = game_data_mobile

    return deepcopy(xbox)

def steam2mobile(data: PresideData) -> PresideDataMobile:
    """
    将 Steam 存档数据转换为移动版（Android）存档数据。
    """
    mobile = PresideDataMobile.new()
    mobile.save_version_ = Int32(1)
    # OptionWorkMobile
    option_work_steam = data.system_data_.option_work_
    option_work_mobile = OptionWorkMobile.new()
    _copy_attr(option_work_steam, option_work_mobile)
    # SystemDataMobile
    system_data_steam = data.system_data_
    system_data_mobile = SystemDataMobile.new()
    _copy_attr(system_data_steam, system_data_mobile)
    system_data_mobile.option_work_ = option_work_mobile
    mobile.system_data_ = system_data_mobile

    # GameDataXbox
    for i, game_data_steam in enumerate(data.slot_list_):
        msg_data_steam = game_data_steam.msg_data_
        msg_data_xbox = MessageDataXbox.new()
        _copy_attr(msg_data_steam, msg_data_xbox)

        game_data_xbox = GameDataXbox.new()
        _copy_attr(game_data_steam, game_data_xbox)
        game_data_xbox.msg_data_ = msg_data_xbox
        mobile.slot_list_[i] = game_data_xbox

    mobile.expansion_data_.is_agree = bool_(1)
    return deepcopy(mobile)

def mobile2steam(data: PresideDataMobile) -> PresideData:
    """
    将移动版（Android）存档数据转换为 Steam 存档数据。\n
    移动版存档中缺少的数据将会从默认空存档中读取。
    """
    steam = PresideData.new()
    default_save = PresideData.from_file(utils.abspath('res/steam_empty_save'))
    # OptionWork
    option_work_mobile = data.system_data_.option_work_
    option_work_steam = OptionWork.new()
    option_work_default = default_save.system_data_.option_work_
    _copy_attr(option_work_default, option_work_steam)
    _copy_attr(option_work_mobile, option_work_steam)
    # SystemData
    system_data_mobile = data.system_data_
    system_data_steam = SystemData.new()
    _copy_attr(system_data_mobile, system_data_steam)
    system_data_steam.option_work_ = option_work_steam
    steam.system_data_ = system_data_steam

    # GameData
    for i, game_data_mobile in enumerate(data.slot_list_):
        msg_data_mobile = game_data_mobile.msg_data_
        msg_data_steam = MessageData.new()
        msg_data_default = default_save.slot_list_[i].msg_data_
        _copy_attr(msg_data_default, msg_data_steam)
        _copy_attr(msg_data_mobile, msg_data_steam)

        game_data_steam = GameData.new()
        _copy_attr(game_data_mobile, game_data_steam)
        game_data_steam.msg_data_ = msg_data_steam
        steam.slot_list_[i] = game_data_steam

    return deepcopy(steam)

if __name__ == '__main__':
    import app.editor.locator as locator
    steam_id, steam_path = locator.system_steam_save_path[0]
    xbox_path = locator.system_xbox_save_path[0]
    # with open(steam_path, 'rb') as f:
    #     steam = PresideData.from_bytes(f.read())
    # xbox = steam2xbox(steam)
    
    xbox = PresideDataXbox.from_file(xbox_path)
    steam = xbox2steam(xbox)
    steam.system_data_.reserve_work_.reserve[1] = Int32(int(steam_id))
    PresideData.to_file(steam, steam_path)
    
    1
    # with open(xbox_path, 'wb') as f:
    #     f.write(PresideDataXbox.to_bytes(xbox))