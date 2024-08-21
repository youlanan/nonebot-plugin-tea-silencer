'''
配置部分
'''
try: import ujson as json
except ImportError: import json
from nonebot import get_plugin_config
from pydantic import BaseModel
from typing import Set, Any, Dict


class ConfigModel(BaseModel):
    # 消息检查开关 为True时禁用插件
    silencer_off: bool = False
    
    # 为True时必须艾特对话才触发
    silencer_at: bool = False
    
    # 为False时仅在框架正常结束时转存黑名单为json 
    # 这将减少部分情况时性能开销，但意外情况下会丢失本次运行期间的黑名单数据
    silencer_safe: bool = True
    
    # 这是一份被格式化为字符串的json，可以通过它来完全自定义任意数值
    # 需要注意：在json中，当键为数值时必须将其写为一个字符串
    silencer_config: str = '''
        {
            "等级规则": {
                "5": ["遇境", 0],
                "100": ["伊甸", 525600]
            },
            "词库分贝": {
                "广告": 5,
                "涩涩": 3,
                "侮辱": 10,
                "建政": 10,
                "非法": 20
            },
            "回复方案": {
                "0": "提示",
                "10": "棉花"
            },
            "记忆阈值": 50,
            "群缩放": 4
        }
    '''

config = get_plugin_config(ConfigModel)
'''配置项'''

silencer_off = config.silencer_off
'''消息检查开关 为True时禁用插件'''

silencer_at = config.silencer_at
'''消息检查开关 为True时必须艾特对话才触发'''

silencer_safe = config.silencer_safe
'''为False时仅程序结束时储存数据'''


def JSON反序列(data: str) -> Dict[Any, Any]:
    '''将 JSON 字符串反序列化为字典，并将数字字符串键转换为整数键'''

    def convert_keys(d: Dict[str, Any]) -> Dict[Any, Any]:
        new_dict = {}
        for key, value in d.items():
            # 转换键
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

    # 解析 JSON 字符串并转换键
    parsed_data = json.loads(data)
    return convert_keys(parsed_data)

silencer_config = JSON反序列(config.silencer_config)
'''配置字典{分贝升等、词库分贝、储存分贝}'''