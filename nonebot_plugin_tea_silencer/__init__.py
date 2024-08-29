'''
高自定义的强效消音器
'''
from .silencer import *
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="消音器",
    description="又一个消息审查插件，可针对不同程度嘴臭配置自动屏蔽、回应规则，支持指令拉黑群或用户。",
    usage="""
    消音 [t 8-12位整数时间] [g 群id] [u 用户id]
    解除消音 [g 群id] [u 用户id]
    添加消音词 [领域] [词 词]
    删除消音词 [词 词]
    """,
    type="application",
    # 发布必填，当前有效类型有：`library`（为其他插件编写提供功能），`application`（向机器人用户提供功能）。
    homepage="https://github.com/youlanan/nonebot-plugin-tea-silencer",
    # 发布必填。
    config=ConfigModel,
    supported_adapters={"~onebot.v11"},
    # 支持的适配器集合，其中 `~` 在此处代表前缀 `nonebot.adapters.`，其余适配器亦按此格式填写。
    # 若插件可以保证兼容所有适配器（即仅使用基本适配器功能）可不填写，否则应该列出插件支持的适配器。
)