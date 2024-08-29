'''
配置部分
'''
try: import ujson as json
except ImportError: import json
from nonebot import get_plugin_config
from pydantic import BaseModel
from typing import Optional, Set, Any, Dict


class ConfigModel(BaseModel):
    '''配置类'''
    
    superusers: Set[str] = []                      # NB的超管配置
    superusers_ignore: bool = False                # 是否忽略超管发言的检查
    silencer_off: bool = False                     # 是否禁用插件
    silencer_at: bool = True                       # 是否需要@对话才触发
    silencer_safe: bool = False                    # 是否频繁保存黑名单到本地文件（False时仅在程序正常结束储存）
    silencer_data_path: Optional[str] = None       # 自定义的配置路径
    
    # 一份字符串格式的json，帮助完全自定义数值。
    silencer_config: str = '''
    {
        "等级规则": {
            "20": ["暮土", 180],
            "45": ["禁阁", 1440],
            "70": ["伊甸", 7200],
            "100": ["暴风眼", 10800]
        },
        "词库分贝": {
            "广告": 3,
            "涩涩": 5,
            "侮辱": 8,
            "键政": 8,
            "非法": 10
        },
        "回复方案": {
            "0": "提示",
            "10": "棉花",
            "30": "阴阳",
            "45": "飞马"
        },
        "记忆阈值": 20,
        "群缩放": 4
    }
    '''

config = get_plugin_config(ConfigModel)
''' 配置项 '''

silencer_off = config.silencer_off
''' 消息检查开关 为 True 时禁用插件 '''

silencer_at = config.silencer_at
''' 消息检查开关 为 True 时必须艾特对话才触发 '''

superusers_ignore = config.superusers_ignore
''' 超管忽略 '''

superusers = config.superusers
''' SUPERUSER '''

silencer_safe = config.silencer_safe
''' 为 False 时仅程序结束时储存数据 '''

silencer_data_path = config.silencer_data_path
''' 为空时默认存放在localstore插件提供目录下 '''


def JSON反序列(data: str) -> Dict[Any, Any]:
    '''
    将 JSON 字符串反序列化为字典
    并将数字字符串键转换为整数键
    '''
    def convert_keys(d: Dict[str, Any]) -> Dict[Any, Any]:
        new_dict = {}
        for key, value in d.items():
            new_key = int(key) if key.isdigit() else key
            # 递归处理子字典
            if isinstance(value, dict):
                new_dict[new_key] = convert_keys(value)
            # 处理子列表
            elif isinstance(value, list):
                new_dict[new_key] = [convert_keys(item) if isinstance(item, dict) else item for item in value]
            else:
                new_dict[new_key] = value
        return new_dict
    parsed_data = json.loads(data)
    return convert_keys(parsed_data)

silencer_config = JSON反序列(config.silencer_config)
''' 配置字典{等级规则、词库分贝、回复方案、记忆阈值、群缩放} '''