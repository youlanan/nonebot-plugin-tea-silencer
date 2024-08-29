'''
本体部分
'''
import re
import shutil
import asyncio
try: import ujson as json
except ImportError: import json
from datetime import datetime, timedelta
from pathlib import Path
from random import random, choice
from typing import Optional
from nonebot import get_driver, require, on_command
from nonebot.log import logger
from nonebot.params import CommandArg, EventToMe
from nonebot.message import event_preprocessor
from nonebot.exception import IgnoredException
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import (
    GroupMessageEvent,
    MessageEvent,
    Message,
    Bot
    )
from .config import *

require("nonebot_plugin_localstore")

import nonebot_plugin_localstore as store


async def 更新JSON(path: Path, content: dict={}) -> None:
    with open(path, 'w', encoding='utf-8') as data:
        json.dump(content, data, ensure_ascii=False, indent=4)


async def 读取JSON(path: Path) -> dict:
    with open(path, 'r', encoding='utf-8') as data:
        content = json.load(data)
    return content


async def 储存JSON(path: Path, file: str, datas: dict = {}, 自检: Optional[bool] = False) -> None:
    async def 路径自检(path: Path) -> None:
        if not path.parent.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        await 路径自检(path)
        if 自检:
            if not path.exists():
                await 更新JSON(path, datas)
                tolog(f"{file} 不存在，已自动创建喵")
            return
        await 更新JSON(path, datas)
        tolog(f"好耶！{file} 储存更新完毕！")
    except Exception as e:
        tolog(f"不好了喵！储存 {file} 出错了喵", e)


def tolog(info: str, e=None) -> None:
    if e:
        logger.error(f"[消音器] {info}: {e}")
        return
    logger.info(f"\033[33m[消音器] {info}\033[0m")


async def 时间转整数(dt: datetime) -> int:
    """将 datetime 对象转换为整数格式"""
    return int(dt.strftime('%Y%m%d%H%M'))


async def 整数转时间(时间: int) -> datetime:
    """将整数格式的时间转换为 datetime 对象"""
    dt_str = str(时间)
    return datetime.strptime(dt_str, '%Y%m%d%H%M')


async def 缓存本地化(阈值: int, 缓存: dict, file: str) -> None:
    ''' 仅保留 **分贝>阈值 | 已被拉黑** 的群或用户 '''
    if not 缓存:
        tolog("当前拦截记录为空，不进行本地化储存喵")
        return
    path: Path = GlobalVar.词库目录 / 'decibel' / f'{file}.json'
    本地化 = {键: 值 for 键, 值 in 缓存.items() if 值[0] >= 阈值 or 值[1] != 0}
    if not 本地化:
        tolog("当前拦截记录均未达阈值，不进行本地化储存喵")
    await 储存JSON(path, file, 本地化)


class GlobalVar:
    ''' 全局变量类 '''
    
    词库目录 = None
    ''' 插件数据存放路径 '''

    用户缓存, 群缓存 = {}, {}
    ''' 短期记忆 {id: [0分贝, 1整数时间|0], 级别} '''
    
    匹配词库 = {key: None for key in ['涩涩', '键政', '非法', '广告', '侮辱']}
    ''' 示例: **if GlobalVar.["涩涩"].search(text):** '''
    
    词库分贝 = {}
    ''' 写入字典提高效率: **{"广告": 5} = 广告领域触发一次+5分贝** '''

    群缩放 = 1
    '''' 该配置仅作用于群聊，将用户升级所需分贝*该变量值以计算群分贝等级 '''
    
    等级规则 = {}
    ''' **100 : ["伊甸", 525600] = 该等级所需分贝: [命名, 屏蔽分钟数]** '''

    记忆阈值 = 0
    ''' 当超过配置的阈值时 缓存内容将转存至本地JSON 
        重启框架等操作将不影响玩家黑名单升级之路“再续前缘” '''
    
    回复词库 = {key: None for key in ['提示', '棉花', '阴阳', '飞马']}
    ''' 示例: **choice(GlobalVar.回复词库["飞马"])** '''

    回复方案 = {}
    ''' **10: "棉花" = 从分贝10开始使用“棉花词库”进行回应 为None时关闭** '''



async def 用户审查(user_id: str, group_id: Optional[str] = None) -> str | None:
    ''' 若在黑名单则屏蔽 '''
    
    群截止 = GlobalVar.群缓存.get(group_id, [0, 0])[1] if group_id else 0
    用户截止 = GlobalVar.用户缓存.get(user_id, [0, 0])[1]

    # 无事放行
    if 群截止 == 用户截止 == 0:
        return None

    现在 = await 时间转整数(datetime.now())

    # 垃圾清理
    def 删除过期缓存(截止时间: int, entity_id: str, cache: dict):
        if 截止时间 > 0 and 现在 - 截止时间 > 0:
            del cache[entity_id]

    if group_id:
        删除过期缓存(群截止, group_id, GlobalVar.群缓存)
    删除过期缓存(用户截止, user_id, GlobalVar.用户缓存)
    
    # 继续屏蔽
    if (group_id and group_id in GlobalVar.群缓存) or (user_id in GlobalVar.用户缓存):
        tolog("已拦截黑名单群或用户的消息喵")
        if random() < 0.3:
            return "哼——！"
        raise IgnoredException("已拦截黑名单群或用户的消息")
    
    return None


async def 消息审查(text: str, user_id: str, group_id: Optional[str] = None) -> list:
    ''' 对有害信息进行相关处理 '''
    # 计算该信息分贝值
    分贝 = sum(GlobalVar.词库分贝[key] for key, regex in GlobalVar.匹配词库.items() if regex.search(text))
    if 分贝 <= 0:
        return []

    tolog("已拦截不安全的消息喵")
    group_id = str(group_id) if group_id else None

    # 初始化缓存（若不存在）
    用户缓存 = GlobalVar.用户缓存.setdefault(user_id, [0, 0, None])
    群缓存 = GlobalVar.群缓存.setdefault(group_id, [0, 0, None]) if group_id else None

    async def 分贝等级查询(分贝: int, group: bool = False) -> Optional[list]:
        if group:
            分贝 //= GlobalVar.群缩放
        return GlobalVar.等级规则.get(max((key for key in GlobalVar.等级规则 if key <= 分贝), default=None))

    def 更新缓存(缓存: list, 分贝: int) -> int:
        缓存[0] += 分贝
        return 缓存[0]

    async def 检查等级并更新缓存(缓存: list, 总分贝: int, 群: bool = False) -> Optional[str]:
        info = await 分贝等级查询(总分贝, group=群)
        if info and info[0] != 缓存[2]:
            缓存[2] = info[0]
            if info[1] > 0:
                缓存[1] = await 时间转整数(datetime.now() + timedelta(minutes=info[1]))
            return f"[消音器] 当前{'群' if 群 else '你'}的分贝已达到‘{info[0]}’级别，" \
                   f"{f'服务结束！我们{info[1]}分钟后见哦~' if info[1] > 0 else '请文明上网，认真生活喵~'}"
        return None

    用户总分贝 = 更新缓存(用户缓存, 分贝)
    用户消息 = await 检查等级并更新缓存(用户缓存, 用户总分贝)

    msg = [用户消息] if 用户消息 else []

    if group_id:
        群总分贝 = 更新缓存(群缓存, 分贝)
        群消息 = await 检查等级并更新缓存(群缓存, 群总分贝, 群=True)
        if 群消息:
            msg.insert(0, 群消息)
    else:
        群总分贝 = None

    if silencer_safe:
        if 用户总分贝 >= GlobalVar.记忆阈值:
            await 缓存本地化(GlobalVar.记忆阈值, GlobalVar.用户缓存, "小黑子")
        if 群总分贝 and 群总分贝 >= GlobalVar.记忆阈值:
            await 缓存本地化(GlobalVar.记忆阈值, GlobalVar.群缓存, "黑子窝")
    
    # 追加回复语
    定义值 = max((key for key in GlobalVar.回复方案 if key <= 用户总分贝), default=None)
    if 定义值 == None:
        raise IgnoredException("已拦截不安全的消息")
    字符键 = GlobalVar.回复方案[定义值]
    词库 = GlobalVar.回复词库.get(字符键, [])
    if not 词库:
        raise IgnoredException("已拦截不安全的消息")
    msg.insert(0, choice(词库))
    return msg



@event_preprocessor
async def 检测(bot: Bot, event: MessageEvent, at: bool = EventToMe()):
    if silencer_off: return
    if silencer_at and not at: return
    text = event.get_plaintext().strip()
    if not text: return
    user_id = event.get_user_id()
    if superusers_ignore and user_id in superusers: return
    group_id = event.group_id if isinstance(event, GroupMessageEvent) else None
    group_id = str(group_id) if group_id else None
    
    
    if echo := await 用户审查(user_id, group_id):
        await bot.send(event = event, message = echo)
        raise IgnoredException("已拦截黑名单群或用户的消息")
    
    if (echo := await 消息审查(text, user_id, group_id)) and len(echo) > 0:
        for msg in echo:
            await bot.send(event = event, message = msg)
        raise IgnoredException("已拦截不安全的消息")



ban = on_command("ban",
                aliases = {"消音", "屏蔽"},
                permission = SUPERUSER)


@ban.handle()
async def _(args: Message = CommandArg()):
    if text := args.extract_plain_text():
        text = text.strip()

        async def 解析参数(text: str) -> tuple[int, list[str], list[str]]:
            时间正则 = re.compile(r't\s*(\d{8}|\d{12})')  # 匹配8或12位的时间整数
            群聊正则 = re.compile(r'g\s*(\d[\d\s\W]*)')   # 匹配字母g后所有连贯的数字和符号
            用户正则 = re.compile(r'u\s*(\d[\d\s\W]*)')   # 匹配字母u后所有连贯的数字和符号

            时间匹配 = 时间正则.search(text)
            if not 时间匹配:
                await ban.finish("\n参数错误: 缺少时间戳或格式不正确。\n正确示例: t202509010030 或 t20250901\n")

            时间字符串 = 时间匹配.group(1)
            if len(时间字符串) == 8:  # 如果是8位，自动补齐成12位
                时间字符串 += "0000"

            时间 = int(时间字符串)

            群聊ID列表 = [str(int(g)) for match in 群聊正则.findall(text) for g in re.findall(r'\d+', match)]
            用户ID列表 = [str(int(u)) for match in 用户正则.findall(text) for u in re.findall(r'\d+', match)]

            if not 群聊ID列表 and not 用户ID列表:
                await ban.finish("\n参数错误: 至少需要一个群聊ID或用户ID。\n正确示例: /ban t20250901 g123456 u123456\n")

            return 时间, 群聊ID列表, 用户ID列表

        async def 更新屏蔽(缓存: dict, ID列表: list[str], 时间: int) -> None:
            for 鸡 in ID列表:
                if 鸡 not in 缓存:
                    缓存[鸡] = [0, 0, None]
                缓存[鸡][1] = 时间

        时间, 群聊ID列表, 用户ID列表 = await 解析参数(text)

        if 群聊ID列表 and len(群聊ID列表) > 0:
            await 更新屏蔽(GlobalVar.群缓存, 群聊ID列表, 时间)
            await 缓存本地化(GlobalVar.记忆阈值, GlobalVar.群缓存, "黑子窝")
            await ban.send(f"成功对 {len(群聊ID列表)} 个群聊进行消音处理！")

        if 用户ID列表 and len(用户ID列表) > 0:
            await 更新屏蔽(GlobalVar.用户缓存, 用户ID列表, 时间)
            await 缓存本地化(GlobalVar.记忆阈值, GlobalVar.用户缓存, "小黑子")
            await ban.finish(f"成功对 {len(用户ID列表)} 个用户进行消音处理！")
    
    await ban.finish(
        "\n参数错误: 如果你想批量封禁 群聊123 和 用户456 到 2025年9月1日" \
        "，则应输入：\n/ban t20250901 g123 u456\n")


unban = on_command("unban",
                aliases = {"deban", "解除屏蔽", "解除消音"},
                permission = SUPERUSER)


@unban.handle()
async def _(args: Message = CommandArg()):
    if text := args.extract_plain_text():
        text = text.strip()

        async def 解析参数(text: str) -> tuple[list[str], list[str]]:
            群聊正则 = re.compile(r'g\s*(\d[\d\s\W]*)')
            用户正则 = re.compile(r'u\s*(\d[\d\s\W]*)')

            # 提取群聊ID列表
            群聊ID列表 = [str(int(g)) for match in 群聊正则.findall(text) for g in re.findall(r'\d+', match)]

            # 提取用户ID列表并转换为字符串
            用户ID列表 = [str(int(u)) for match in 用户正则.findall(text) for u in re.findall(r'\d+', match)]

            if not 群聊ID列表 and not 用户ID列表:
                await unban.finish("\n参数错误: 至少需要一个群聊ID或用户ID。\n正确示例: /unban g123456 u123456\n")

            return 群聊ID列表, 用户ID列表

        async def 解除屏蔽(缓存: dict, ID列表: list[str]) -> None:
            no = ''
            for 尼 in ID列表:
                if 尼 not in 缓存:
                    no += f'{尼} '
                else:
                    del 缓存[尼]
            return no
        
        群聊ID列表, 用户ID列表 = await 解析参数(text)

        if 群聊ID列表 and len(群聊ID列表) > 0:
            no = await 解除屏蔽(GlobalVar.群缓存, 群聊ID列表)
            await 缓存本地化(GlobalVar.记忆阈值, GlobalVar.群缓存, "黑子窝")
            await unban.send(f"群聊：{no}未被拦截，请检查输入") if no else await unban.send(f"群聊成功解除消音！")

        if 用户ID列表 and len(用户ID列表) > 0:
            no = await 解除屏蔽(GlobalVar.用户缓存, 用户ID列表)
            await 缓存本地化(GlobalVar.记忆阈值, GlobalVar.用户缓存, "小黑子")
            await unban.finish(f"用户：{no}未被拦截，请检查输入") if no else await unban.finish(f"用户成功解除消音！")
        
        return

    await unban.finish(
        "\n参数错误: 如果你想批量解封 群聊123 和 用户456、789" \
        "，则应输入：\n/unban g123 u456 789\n")


addf = on_command("addf",
                aliases = {"添加屏蔽词", "添加消音词"},
                permission = SUPERUSER)


@addf.handle()
async def _(args: Message = CommandArg()):
    if text := args.extract_plain_text():
        text = text.strip()

        async def 解析参数(text: str, 匹配词库: dict) -> tuple[str, list[str]]:
            参数列表 = text.split()

            if not 参数列表:
                await addf.finish("指令参数不能为空")

            第一参数 = 参数列表[0]

            if 第一参数 not in 匹配词库:
                await addf.finish(f"\n未指定要添加的词库！\n如果你想向涩涩词库中添加一些屏蔽词，则应输入：\n/addf 涩涩 xx xx\n")

            剩余参数 = 参数列表[1:] if len(参数列表) > 1 else []

            return 第一参数, 剩余参数

        async def 合并去重(list1: list, list2: list) -> list:
            汇总 = list1 + list2
            去重 = list(dict.fromkeys(汇总))
            return 去重

        第一参数, 追加词库 = await 解析参数(text, GlobalVar.匹配词库)
        if 追加词库:
            原词库 = await 载入消音词(第一参数)
            新词库 = await 合并去重(原词库, 追加词库)
            GlobalVar.匹配词库[第一参数] = re.compile('|'.join(map(re.escape, 新词库)))
            path: Path = GlobalVar.词库目录 / 'filter' / f'{第一参数}.json'
            await 储存JSON(path, 第一参数, {f"{第一参数}": 新词库})
            tolog(f"已向 {第一参数} 词库中新增了 {len(追加词库)} 个消音词")
            await addf.finish(f"已向 {第一参数} 词库中新增了 {len(追加词库)} 个消音词")

    await addf.finish(
        "\n参数错误: 如果你想批量添加屏蔽词，则应输入：\n/addf 涩涩 xx xx\n")


delf = on_command("delf",
                aliases = {"删除屏蔽词", "删除消音词"},
                permission = SUPERUSER)


@delf.handle()
async def _(args: Message = CommandArg()):
    if text := args.extract_plain_text():
        text = text.strip()

        async def 解析参数(text: str) -> list:
            参数列表 = text.split()

            if not 参数列表:
                await delf.finish("指令参数不能为空")

            return 参数列表

        删除词库 = await 解析参数(text)
        if 删除词库:
            改 = 0
            for key in GlobalVar.匹配词库:
                校对 = 词库 = await 载入消音词(key)
                新词库 = [x for x in 词库 if x not in 删除词库]
                if 新词库 == 校对:
                    continue
                改 += 1
                GlobalVar.匹配词库[key] = re.compile('|'.join(map(re.escape, 新词库)))
                path: Path = GlobalVar.词库目录 / 'filter' / f'{key}.json'
                await 储存JSON(path, key, {f"{key}": 新词库})
            tolog(f"删除消音词操作成功！共修改 {改} 个词库。")
            await delf.finish(f"删除消音词操作成功！共修改 {改} 个词库。")

    await delf.finish(
        "\n参数错误: 如果你想批量删除屏蔽词，则应输入：\n/delf xx xx\n")



async def 载入回复语(file: str) -> list:
    path: Path = GlobalVar.词库目录 / 'flymo' / f'{file}.json'
    try:
        content = await 读取JSON(path)
        words = content[file]
        tolog(f"载入 {file} 回复语 x{len(words)}！")
        return words
    except Exception as e:
        tolog(f"载入 {file} 回复语时出现意外情况", e)
        return ["已过滤, Filter"]


async def 载入消音词(file: str) -> list:
    path: Path = GlobalVar.词库目录 / 'filter' / f'{file}.json'
    try:
        content = await 读取JSON(path)
        words = content[file]
        tolog(f"载入 {file} 消音词 x{len(words)}！")
        if not words or len(words) <= 0:
            return ["test1消音"]
        return words
    except Exception as e:
        tolog(f"载入 {file} 消音词时出现意外情况", e)
        return ["test1消音"]


async def 载入用户数据(file: str) -> dict:
    path: Path = GlobalVar.词库目录 / 'decibel' / f'{file}.json'
    if not path.exists():
        return {}
    try:
        content = await 读取JSON(path)
        tolog(f"载入 {file} 数据 x{len(content)}！")
        return content
    except Exception as e:
        tolog(f"载入 {file} 消音词时出现意外情况", e)
        return {}



driver = get_driver()


@driver.on_startup
async def _():
    def 数据路径(配置转存: str):
        tolog("正在加载插件数据")
        安装路径 = Path(__file__).parent / "silencer"
        # 默认路径: Path = Path.cwd() / "data" / "silencer"
        # plugin_data_dir: Path = store.get_plugin_data_dir()
        plugin_data = store.get_data_dir("nonebot_plugin_tea_silencer")
        插件数据: Path = plugin_data / "silencer"
        
        if 配置转存:
            tolog("检测到自定义词库储存路径，请确保数据文件存在于指向目录")
            return Path(配置转存)
        
        elif 安装路径.is_dir() and not 插件数据.is_dir():
            tolog(f"初始化，正在迁移插件数据至本地目录: \nfrom {安装路径} -> \nto {插件数据}")
            插件数据.mkdir(parents=True, exist_ok=True)
            shutil.copytree(安装路径, 插件数据, dirs_exist_ok=True)
            shutil.rmtree(安装路径)
            return 插件数据
        
        elif 插件数据.is_dir():
            return 插件数据
        
        else:
            tolog("载入插件词库时出错", f"找不到数据储存路径")
            return None
    
    GlobalVar.词库目录 = 数据路径(silencer_data_path)
    
    
    async def 配置自检():
        配置列表 = {
            'filter': ['涩涩', '键政', '非法', '广告', '侮辱'],
            'flymo': ['提示', '棉花', '阴阳', '飞马']
        }
        tasks = [
            储存JSON(GlobalVar.词库目录 / 目录 / f'{文件名}.json', 文件名, {文件名: []}, 自检=True)
            for 目录, 文件名列表 in 配置列表.items()
            for 文件名 in 文件名列表
        ]
        await asyncio.gather(*tasks)

    async def 编译正则(words: list) -> re.Pattern:
        return re.compile('|'.join(map(re.escape, words)))

    async def 加载正则(key: str):
        return await 编译正则(await 载入消音词(key))

    await 配置自检()

    # 并发加载所有的正则表达式和回复语，优化加载效率
    GlobalVar.匹配词库['涩涩'], GlobalVar.匹配词库['键政'], GlobalVar.匹配词库['非法'], \
    GlobalVar.匹配词库['广告'], GlobalVar.匹配词库['侮辱'] = await asyncio.gather(
        加载正则('涩涩'),
        加载正则('键政'),
        加载正则('非法'),
        加载正则('广告'),
        加载正则('侮辱')
    )

    GlobalVar.回复词库['提示'], GlobalVar.回复词库['棉花'], GlobalVar.回复词库['阴阳'], \
    GlobalVar.回复词库['飞马'] = await asyncio.gather(
        载入回复语('提示'),
        载入回复语('棉花'),
        载入回复语('阴阳'),
        载入回复语('飞马')
    )

    # 同步加载配置数据
    config = silencer_config
    GlobalVar.词库分贝 = config["词库分贝"]
    GlobalVar.等级规则 = config["等级规则"]
    GlobalVar.回复方案 = config["回复方案"]
    GlobalVar.记忆阈值 = config["记忆阈值"]
    GlobalVar.群缩放 = config["群缩放"]

    asyncio.gather(
        载入用户数据('小黑子'),
        载入用户数据('黑子窝'),
    )


@driver.on_shutdown
async def _():
    await 缓存本地化(GlobalVar.记忆阈值, GlobalVar.用户缓存, "小黑子")
    await 缓存本地化(GlobalVar.记忆阈值, GlobalVar.群缓存, "黑子窝")