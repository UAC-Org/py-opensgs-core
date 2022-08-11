from nonebot import on_command, on_message
from nonebot.adapters import Bot
from nonebot.rule import to_me
from nonebot.adapters.cqhttp.event import GroupMessageEvent
from nonebot.adapters.cqhttp.message import Message
import random

def get_key(d:dict, value):#反查
    k = [k for k, v in d.items() if v == value]
    return k

playerlist = {}
playergeneral = {}
playerlives = {}
playercards = {}
playeridentity = {}
playerblock = {}
playerequipment = {}
playerlifemax = {}
dieplayers = []
identity = ["反贼", "忠臣"]
generals = {"硝酸钠":4, "小ming":4, "Miku":3, "瑄瑄啊":2, "阿云":4, "pui":5, "群主姐姐":4, "高铁":4, "U235":4, "星雨":4, "大白":4, 
"南周白明":4, "nb":4, "标·硝酸钠":4, "神·硝酸钠":4}
card_list = ["黑桃7 杀", "黑桃8 杀", "黑桃Ⅷ 杀", "黑桃Ⅸ 杀", "黑桃9 杀", "黑桃X 杀", "黑桃10 杀", "梅花 2 杀", "梅花3 杀", "梅花4 杀",
"梅花5 杀", "梅花6 杀", "梅花7 杀", "梅花8 杀", "梅花Ⅷ 杀", "梅花9 杀", "梅花Ⅸ 杀", "梅花10 杀", "梅花X 杀", "梅花J 杀", "梅花11 杀", "红桃10 杀",
"红桃X 杀", "红桃J 杀", "方块6 杀", "方块7 杀", "方块8 杀", "方块9 杀", "方块10 杀", "方块K 杀", "红桃4 火杀", "红桃7 火杀", "红桃10 火杀", "方块4 火杀",
"方块5 火杀", "黑桃4 雷杀", "黑桃5 雷杀", "黑桃6 雷杀", "黑桃7 雷杀", "黑桃8 雷杀", "梅花5 雷杀", "梅花6 雷杀", "梅花7 雷杀", "梅花8 雷杀", "黑桃3 过河拆桥",
"黑桃4 过河拆桥","黑桃Q 过河拆桥", "梅花3 过河拆桥", "梅花4 过河拆桥","红桃Q 过河拆桥", "黑桃3 顺手牵羊", "黑桃4 顺手牵羊", "黑桃J 顺手牵羊", "方块3 顺手牵羊",
"方块4 顺手牵羊", "黑桃A 决斗", "梅花A 决斗", "方块A 决斗", "梅花Q 借刀杀人", "梅花K 借刀杀人", "红桃7 无中生有", "红桃8 无中生有", "红桃9 无中生有", 
"红桃J 无中生有", "黑桃J 无懈可击", "黑桃K 无懈可击", "梅花Q 无懈可击", "梅花K 无懈可击", "红桃A 无懈可击", "红桃K 无懈可击", "方块Q 无懈可击", "黑桃J 铁索连环", 
"黑桃Q 铁索连环", "梅花10 铁索连环", "梅花J 铁索连环","梅花Q 铁索连环", "梅花K 铁索连环", "红桃2 火攻", "红桃3 火攻", "方块Q 火攻", "红桃A 万箭齐发", "黑桃7 南蛮入侵",
"黑桃K 南蛮入侵", "梅花7 南蛮入侵", "红桃A 桃园结义", "红桃3 五谷丰登", "红桃4 五谷丰登", "黑桃A 闪电","红桃Q 闪电", "黑桃6 乐不思蜀", "红桃6 乐不思蜀",
"梅花6 乐不思蜀","黑桃10 兵粮寸断","梅花4 兵粮寸断","梅花A 诸葛连弩","方片A 诸葛连弩","黑桃6 青釭剑","黑桃2 雌雄双股剑","黑桃2 寒冰剑","黑桃A 古锭刀","方块5 贯石斧","黑桃5 青龙偃月刀","黑桃Q 丈八蛇矛",
"方块Q 方天画戟","方块A 朱雀羽扇","红桃A 麒麟弓","方块Q 银月枪","黑桃2 八卦阵","梅花2 八卦阵","梅花2 仁王盾","黑桃2 藤甲","梅花2 藤甲","梅花A 白银狮子",
"黑桃5 +1马","红桃K +1马","方块K +1马","梅花5 +1马","黑桃K -1马","红桃5 -1马","方块K -1马","方块5 木牛流马"]
card_list_backup = ["黑桃7 杀", "黑桃8 杀", "黑桃Ⅷ 杀", "黑桃Ⅸ 杀", "黑桃9 杀", "黑桃X 杀", "黑桃10 杀", "梅花 2 杀", "梅花3 杀", "梅花4 杀",
"梅花5 杀", "梅花6 杀", "梅花7 杀", "梅花8 杀", "梅花Ⅷ 杀", "梅花9 杀", "梅花Ⅸ 杀", "梅花10 杀", "梅花X 杀", "梅花J 杀", "梅花11 杀", "红桃10 杀",
"红桃X 杀", "红桃J 杀", "方块6 杀", "方块7 杀", "方块8 杀", "方块9 杀", "方块10 杀", "方块K 杀", "红桃4 火杀", "红桃7 火杀", "红桃10 火杀", "方块4 火杀",
"方块5 火杀", "黑桃4 雷杀", "黑桃5 雷杀", "黑桃6 雷杀", "黑桃7 雷杀", "黑桃8 雷杀", "梅花5 雷杀", "梅花6 雷杀", "梅花7 雷杀", "梅花8 雷杀", "黑桃3 过河拆桥",
"黑桃4 过河拆桥","黑桃Q 过河拆桥", "梅花3 过河拆桥", "梅花4 过河拆桥","红桃Q 过河拆桥", "黑桃3 顺手牵羊", "黑桃4 顺手牵羊", "黑桃J 顺手牵羊", "方块3 顺手牵羊",
"方块4 顺手牵羊", "黑桃A 决斗", "梅花A 决斗", "方块A 决斗", "梅花Q 借刀杀人", "梅花K 借刀杀人", "红桃7 无中生有", "红桃8 无中生有", "红桃9 无中生有", 
"红桃J 无中生有", "黑桃J 无懈可击", "黑桃K 无懈可击", "梅花Q 无懈可击", "梅花K 无懈可击", "红桃A 无懈可击", "红桃K 无懈可击", "方块Q 无懈可击", "黑桃J 铁索连环", 
"黑桃Q 铁索连环", "梅花10 铁索连环", "梅花J 铁索连环","梅花Q 铁索连环", "梅花K 铁索连环", "红桃2 火攻", "红桃3 火攻", "方块Q 火攻", "红桃A 万箭齐发", "黑桃7 南蛮入侵",
"黑桃K 南蛮入侵", "梅花7 南蛮入侵", "红桃A 桃园结义", "红桃3 五谷丰登", "红桃4 五谷丰登", "黑桃A 闪电","红桃Q 闪电", "黑桃6 乐不思蜀", "红桃6 乐不思蜀",
"梅花6 乐不思蜀","黑桃10 兵粮寸断","梅花4 兵粮寸断","梅花A 诸葛连弩","方片A 诸葛连弩","黑桃6 青釭剑","黑桃2 雌雄双股剑","黑桃2 寒冰剑","黑桃A 古锭刀","方块5 贯石斧","黑桃5 青龙偃月刀","黑桃Q 丈八蛇矛",
"方块Q 方天画戟","方块A 朱雀羽扇","红桃A 麒麟弓","方块Q 银月枪","黑桃2 八卦阵","梅花2 八卦阵","梅花2 仁王盾","黑桃2 藤甲","梅花2 藤甲","梅花A 白银狮子",
"黑桃5 +1马","红桃K +1马","方块K +1马","梅花5 +1马","黑桃K -1马","红桃5 -1马","方块K -1马","方块5 木牛流马"]
equipment=["梅花A 诸葛连弩","方片A 诸葛连弩","黑桃6 青釭剑","黑桃2 雌雄双股剑","黑桃2 寒冰剑","黑桃A 古锭刀","方块5 贯石斧","黑桃5 青龙偃月刀","黑桃Q 丈八蛇矛",
"方块Q 方天画戟","方块A 朱雀羽扇","红桃A 麒麟弓","方块Q 银月枪","黑桃2 八卦阵","梅花2 八卦阵","梅花2 仁王盾","黑桃2 藤甲","梅花2 藤甲","梅花A 白银狮子",
"黑桃5 +1马","红桃K +1马","方块K +1马","梅花5 +1马","黑桃K -1马","红桃5 -1马","方块K -1马","方块5 木牛流马"]

all_cards = len(card_list)
#以上内容翻译即可
block = False#能否加入游戏
block_2 = True#是否选择武将
block_3 = True#是否分发身份
block_4 = True#是否进入第一轮
block_5 = True#是否开始每轮更替
i = 0#第一轮人数统计&每一轮轮流人员
F = 1#每一轮轮流人员

call_up = on_command("加入三国杀", rule = to_me(), priority = -3, block = False)#
start = on_command("开始三国杀", rule = to_me(), priority = -3, block = False)#
stop = on_command("关闭三国杀", rule = to_me(), block = True, priority = -5)#
logout = on_command("退出三国杀", rule = to_me(), block = True, priority = -5)#
choose_general = on_message(rule = to_me(), priority = -4, block = False)#
choose_identity = on_message(priority = -2, block = False)#
licensing_first_round = on_message(priority = -2, block = False)#
licensing_every_round = on_command("过", rule = to_me(), block = False, priority = -2)#
play_cards = on_message(block = False, priority = -3)#
give_up_card = on_command("弃牌", rule = to_me(), block = False)#
get_card = on_command("抽牌", rule = to_me(), block = False)#
cut_lives = on_command("扣血", rule = to_me(), block = False)#
add_lives = on_command("加血", rule = to_me(), block = False)#
cut_max = on_command("扣上限", rule = to_me(), block = False)#
add_max = on_command("加上限", rule = to_me(), block = False)#
add_equipment = on_command("装备", rule = to_me(), block = False)#
cut_equipment = on_command("卸装备", rule = to_me(), block = False)#
judge = on_command("判定", rule = to_me(), block = False)#
draw = on_command("抽取", rule = to_me(), block = False)#
help_ktt = on_command("帮助-三国杀", rule = to_me(), block = False)#
status = on_command("我的状态", aliases = {"sta", "状态"}, rule = to_me(), block = False)#
status_all = on_command("全场状态", aliases = {"asta", "a状态"}, rule = to_me(), block = False)#

@status_all.handle()
async def staa(bot:Bot, event:GroupMessageEvent):
    group_id = str(event.group_id)
    if group_id != "441320920":
        return
    if (len(list(playerlist.keys()))) <= 0:
        await status_all.send("已经没有人了……\n可以用'@我 + 关闭三国杀'指令重开三国杀")
    msg = ""
    msg += "现存 %s 人, 他们是:\n"%(str(len(list(playerlist.keys()))))
    for x in list(playerlist.keys()):
        msg = msg + " #%s [CQ:at,qq=%s]: %s, 血量: %s/%s "%(playerlist[x], x, playergeneral[x], playerlives[x], playerlifemax[x]) + "\n"
    await status_all.send(Message(msg))

@help_ktt.handle()
async def hkt(bot:Bot, event:GroupMessageEvent):
    group_id = str(event.group_id)
    if group_id != "441320920":
        return
    usr_id = str(event.user_id)
    msg = "[CQ:at,qq=%s] 欢迎您参与三国杀, 我将会提供如下帮助qwq:\n1.加入三国杀: 可以@我并发加入三国杀(游戏开始后无法加入)\n2.开始三国杀: 第一位加入三国杀的可以开始三国杀\n3.参与游戏: 可以随时@我说抽取(抽别人的牌), 抽牌(抽牌堆的牌), 加血, 扣血, 加上限, 扣上限, 装备, 卸装备, 以指令'过'为开启下一轮的指令"%(usr_id)
    await help_ktt.send(Message(msg))

@draw.handle()
async def dra(bot:Bot, event:GroupMessageEvent):
    group_id = str(event.group_id)
    if group_id != "441320920":
        return
    usr_id = str(event.user_id)
    msg = str(event.message)
    get = random.randint(0,len(playercards[msg])-1)
    all = playercards[msg][get]
    playercards[usr_id].append(all)
    playercards[msg].remove(all)
    await bot.call_api("send_private_msg", user_id = msg, message = "对方抽取了你的 [%s] "%(all))
    await bot.call_api("send_private_msg", user_id = usr_id, message = "你抽取了对方的的 [%s] "%(all))
    await draw.send(Message("[CQ:at,qq=%s]成功抽取了 [CQ:at,qq=%s] 的牌"%(usr_id, msg)))

@judge.handle()
async def jud(bot:Bot, event:GroupMessageEvent):
    global all_cards, card_list
    group_id = str(event.group_id)
    if group_id != "441320920":
        return
    usr_id = str(event.user_id)
    card = str(card_list[random.randint(0, all_cards-1)])
    await judge.send(Message("[CQ:at,qq=%s]所抽中的判定牌为: %s"%(usr_id, card)))

@cut_equipment.handle()
async def ce(bot:Bot, event:GroupMessageEvent):
    global playerequipment,playercards
    group_id = str(event.group_id)
    if group_id != "441320920":
        return
    usr_id = str(event.user_id)
    msg = str(event.message)
    if msg not in playerequipment[usr_id]:
        await cut_equipment.send(Message("[CQ:at,qq=%s]您甚至没有装备它, 卸不下来…… "%(usr_id)))
    else:
        equipment.append(msg)
        playercards[usr_id].append(msg)
        await cut_equipment.send(Message("[CQ:at,qq=%s] [%s] 成功卸下! "%(usr_id, msg)))

@add_equipment.handle()
async def ae(bot:Bot, event:GroupMessageEvent):
    global playerequipment,playercards
    group_id = str(event.group_id)
    if group_id != "441320920":
        return
    usr_id = str(event.user_id)
    msg = str(event.message)
    if usr_id in dieplayers:
        await give_up_card.send(Message("[CQ:at,qq=%s]您已被判定为死亡, 无法继续装备了! "%(usr_id)))
    if msg not in equipment:
        await add_equipment.send(Message("[CQ:at,qq=%s]装备不存在或已经被他人装备qwq"%(usr_id)))
    else:
        if msg not in playercards[usr_id]:
            await add_equipment.send(Message("[CQ:at,qq=%s]您没有这个装备呢! "%(usr_id)))
            return
        playerequipment[usr_id].append(msg)
        equipment.remove(msg)
        playercards[usr_id].remove(msg)
        await add_equipment.send(Message("[CQ:at,qq=%s] [%s] 装备成功! "%(usr_id, msg)))

@status.handle()
async def sta(bot:Bot, event:GroupMessageEvent):
    global playergeneral,playerequipment,playerlifemax,playerlist,playerlives
    group_id = str(event.group_id)
    if group_id != "441320920":
        return
    usr_id = str(event.user_id)
    s_msg = ""
    s_msg += "您的装备: %s \n"%(playerequipment[usr_id])
    s_msg += "您的血量: %s/%s \n"%(playerlives[usr_id], playerlifemax[usr_id])
    s_msg += "您的武将: %s \n"%(playergeneral[usr_id])
    s_msg += "您所持有的牌数: %s\n"%(len(list(playercards[usr_id])))
    s_msg += "你的所有牌已经通过私信发给您"
    ss_msg = ""
    for x in playercards[usr_id]:
        ss_msg = ss_msg + x + "\n"
    await status.send(Message("[CQ:at,qq=%s]\n%s"%(usr_id, s_msg)))
    await bot.call_api("send_private_msg", user_id = usr_id, message = "您所持有的牌为:\n%s"%(ss_msg))

@add_max.handle()
async def al(bot:Bot, event:GroupMessageEvent):
    global playerlives,playerlifemax
    group_id = str(event.group_id)
    if group_id != "441320920":
        return
    usr_id = str(event.user_id)
    msg = str(event.message)
    try:
        add = int(msg)
        playerlifemax[usr_id] += add
        if playerlives[usr_id] >= playerlifemax[usr_id]:
            playerlives[usr_id] = playerlifemax[usr_id]
        await add_max.send(Message("[CQ:at,qq=%s]成功加上限, 您当前血量为 %s/%s ! "%(usr_id, playerlives[usr_id], playerlifemax[usr_id])))
    except:
        await add_max.send("请输入int整型值哟~")

@cut_max.handle()
async def cl(bot:Bot, event:GroupMessageEvent):
    global playerblock,dieplayers,playeridentity,playerlives,playerlifemax
    group_id = str(event.group_id)
    if group_id != "441320920":
        return
    usr_id = str(event.user_id)
    msg = str(event.message)
    try:
        cut = int(msg)
        if msg < 0:
            await cut_lives.send(Message("[CQ:at,qq=%s]别反着来了亲 ("%(usr_id)))
            return
        if playerlifemax[usr_id] or playerlifemax[usr_id] - cut < 2:
            await cut_max.send(Message("[CQ:at,qq=%s]您再扣上限就没了 ("%(usr_id)))
            return
        playerlifemax[usr_id] -= cut
        if playerlives[usr_id] >= playerlifemax[usr_id]:
            playerlives[usr_id] = playerlifemax[usr_id]
        await cut_max.send(Message("[CQ:at,qq=%s]成功扣上限, 您当前血量为 %s/%s ! "%(usr_id, playerlives[usr_id], playerlifemax[usr_id])))
    except:
        await cut_max.send("请输入int整型值哟~")

@add_lives.handle()
async def al(bot:Bot, event:GroupMessageEvent):
    global playerlives,playerlifemax
    group_id = str(event.group_id)
    if group_id != "441320920":
        return
    usr_id = str(event.user_id)
    msg = str(event.message)
    try:
        add = int(msg)
        if msg < 0:
            await cut_lives.send(Message("[CQ:at,qq=%s]您搁着扣血呢? "%(usr_id)))
            return
        playerlives[usr_id] += add
        if playerlives[usr_id] >= playerlifemax[usr_id]:
            playerlives[usr_id] = playerlifemax[usr_id]
        await add_lives.send(Message("[CQ:at,qq=%s]成功加血, 您当前血量为 %s/%s ! "%(usr_id, playerlives[usr_id], playerlifemax[usr_id])))
    except:
        await add_lives.send("请输入int整型值哟~")

@cut_lives.handle()
async def cl(bot:Bot, event:GroupMessageEvent):
    global playerblock,dieplayers,playeridentity,playerlives,playerlifemax
    group_id = str(event.group_id)
    if group_id != "441320920":
        return
    usr_id = str(event.user_id)
    msg = str(event.message)
    try:
        cut = int(msg)
        if msg < 0:
            await cut_lives.send(Message("[CQ:at,qq=%s]您搁着回血呢? "%(usr_id)))
            return
        playerlives[usr_id] -= cut
        await cut_lives.send(Message("[CQ:at,qq=%s]成功扣血, 您当前血量为 %s/%s ! "%(usr_id, playerlives[usr_id], playerlifemax[usr_id])))
        if(playerlives[usr_id]) <= 0:
            dieplayers.append(usr_id)
            await cut_lives.send(Message("[CQ:at,qq=%s]死了, 他的身份是 %s ! "%(usr_id,playeridentity[usr_id])))
            for x in playercards[usr_id]:
                card_list.append(x)
            for x in playerequipment[usr_id]:
                card_list.append(x)
                equipment.append(x)
            playerequipment.pop(usr_id)
            playercards.pop(usr_id)
            playerlist.pop(usr_id)
            playerblock.pop(usr_id)
            playergeneral.pop(usr_id)
    except:
        await cut_lives.send("请输入int整型值哟~")

@give_up_card.handle()
async def guc(bot:Bot, event:GroupMessageEvent):
    group_id = str(event.group_id)
    if group_id != "441320920":
        return
    msg = str(event.message)
    usr_id = str(event.user_id)
    if usr_id in dieplayers:
        await give_up_card.send(Message("[CQ:at,qq=%s]您已被判定为死亡, 无法继续弃牌了! "%(usr_id)))
    elif msg in playercards[usr_id]:
        playercards[usr_id].remove(msg)
        card_list.append(msg)
        await give_up_card.send(Message("[CQ:at,qq=%s]弃置 [%s] 手牌成功"%(usr_id, msg)))
    else:
        await give_up_card.send(Message("[CQ:t,qq=%s]弃置失败, 您可能没有该手牌呢……"%(usr_id)))

@get_card.handle()
async def gc(bot:  Bot, event:GroupMessageEvent):
    global card_list, playercards, all_cards
    group_id = str(event.group_id)
    if group_id != "441320920":
        return
    msg = str(event.message)
    usr_id = str(event.user_id)
    if usr_id in dieplayers:
        await get_card.send(Message("[CQ:at,qq=%s]您已被判定为死亡, 无法继续抽牌了! "%(usr_id)))
        return
    try:
        card_tmp = []
        all = int(msg)
        for i in range(0, all):
            card = str(card_list[random.randint(0, all_cards-1)])
            card_tmp.append(card)
            card_list.remove(card)
            all_cards = len(card_list)
            playercards[usr_id].append(card)
        card_tmp = playercards[usr_id]
        s_msg = ""
        for x in card_tmp:
            s_msg = s_msg + x + "\n"
        await bot.call_api("send_private_msg", user_id = usr_id, message = "您的所有牌为: \n%s"%(s_msg))
        await get_card.send(Message("[CQ:at,qq=%s]抽取成功!"%(usr_id)))
    except:
        await get_card.send("请输入int整型数字~")

@licensing_every_round.handle()
async def ler(bot:Bot,event:GroupMessageEvent):
    global block_4,all_cards,playerlist,card_list,playercards,block_5,F,playerlives
    new_list = []
    block_5 = True
    group_id = str(event.group_id)
    if group_id != "441320920":
        return
    usr_id = str(event.user_id)
    print(F)
    print(get_key(playerlist, F))
    #print(dieplayers)
    F += 1
    print(F)
    print(get_key(playerlist, F))
    new_list = list(playerlist.values())
    new_list.sort(reverse = True)
    print(new_list)
    if(F > new_list[0]):
        F = 1
    print(F)
    print(get_key(playerlist, F))
    if playerblock[usr_id]:
        print(len(playercards[usr_id]))
        if int(playerlives[usr_id]) < len(playercards[usr_id]):
            await licensing_every_round.send(Message("[CQ:at,qq=%s]您的血量为 %s ,您的手牌数为 %s 需要弃掉 %s 张手牌"%(usr_id, playerlives[usr_id], len(playercards[usr_id]), (len(playercards[usr_id]) - playerlives[usr_id]))))
            block_5 = False
            return
        card_tmp = []
        playerblock[usr_id] = False
        playerblock[get_key(playerlist, F)[0]] = True
        for k in (list(playerlist.keys())):
            if playerblock[k]:
                for j in range(2):
                    card = str(card_list[random.randint(0, all_cards-1)])
                    card_tmp.append(card)
                    card_list.remove(card)
                    all_cards = len(card_list)
                    playercards[k].append(card)                    
                card_tmp = playercards[k]
                s_msg = ""
                for x in card_tmp:
                    s_msg = s_msg + x + "\n"
                await bot.call_api("send_private_msg", user_id = k, message = "您所有的牌为:\n%s"%(s_msg))
                await licensing_every_round.send(Message("现在是[CQ:at,qq=%s]的出牌时间"%(k)))
                print(F)
                block_5 = False
                return

@play_cards.handle()
async def pc(bot:Bot, event:GroupMessageEvent):
    global block_4,all_cards,playerlist,card_list,playercards,block_5,i
    usr_id = str(event.user_id)
    msg = str(event.message)
    group_id = str(event.group_id)
    if group_id != "441320920":
        return
    elif block_5:
        return
    elif usr_id not in list(playerlist.keys()):
        return
    elif not playerblock[usr_id]:
        return
    elif msg not in card_list_backup:
        print("NO")
        return
    else:
        card_tmp = playercards[usr_id]
        if msg in card_tmp:
            card_tmp.remove(msg)
            playercards[usr_id] = card_tmp
            card_list.append(msg)
            await play_cards.send(Message("[CQ:at,qq=%s][%s]已经打出!"%(usr_id, msg)))
        else:
             await play_cards.send(Message("[CQ:at,qq=%s]没有这张牌呢..."%(usr_id)))

@licensing_first_round.handle()
async def lfr(bot:Bot, event:GroupMessageEvent):
    global block_4,all_cards,playerlist,card_list,playercards,block_5,i
    group_id = str(event.group_id)
    if group_id != "441320920":
        return
    if block_4:
        return
    #print("OK")
    i = 0
    for k in list(playerlist.keys()):
        card_tmp = []
        playercards[k] = []
        for j in range(4):
            card = str(card_list[random.randint(0, all_cards-1)])
            card_tmp.append(card)
            card_list.remove(card)
            all_cards = len(card_list)
            playercards[k].append(card)
        s_msg = ""
        for x in card_tmp:
            s_msg = s_msg + x + "\n"
        await bot.call_api("send_private_msg", user_id = k, message = "您第一轮所抽到的牌为: \n%s"%(s_msg))
    await licensing_first_round.send("牌面发放完毕, 现在开始出牌")
    await licensing_first_round.send(Message("现在是[CQ:at,qq=%s]的出牌时间"%(get_key(playerlist, 1)[0])))
    card_tmp = []
    for k in (list(playerlist.keys())):
        if playerblock[k]:
            for j in range(2):
                card = str(card_list[random.randint(0, all_cards-1)])
                card_tmp.append(card)
                card_list.remove(card)
                all_cards = len(card_list)
                playercards[k].append(card)
            card_tmp = playercards[k]
            s_msg = ""
            for x in card_tmp:
                s_msg = s_msg + x + "\n"
            print("%s\n%s"%(k, s_msg))
            await bot.call_api("send_private_msg", user_id = k, message = "您所有的牌为: \n%s"%(s_msg))
    block_4 = True
    block_5 = False

@choose_identity.handle()
async def ci(bot:Bot, event:GroupMessageEvent):
    group_id = str(event.group_id)
    if group_id != "441320920":
        return
    global playerlist,i,playergeneral,playerlives,block_3,identity,block_2
    if block_3:
        return
    playerlist_tmp = list(playerlist.keys())
    random.shuffle(playerlist_tmp)
    random.shuffle(playerlist_tmp)
    for j in range(0,len(playerlist_tmp)):
        playerlist[playerlist_tmp[j]] = j+1
    rebel_count = (len(list(playerlist.keys()))) // 2
    loyal_count = (len(list(playerlist.keys()))) - 2 - rebel_count
    king = get_key(playerlist, 1)
    traitor = get_key(playerlist, 2)
    print(king)
    await choose_identity.send(Message("[CQ:at,qq=%s]的身份是主公"%(king[0])))
    playeridentity[king[0]] = "主公"
    playeridentity[traitor[0]] = "内奸"
    playerblock[king[0]] = True
    for j in list(playerlist.values()):
        if get_key(playerlist, j)[0] == king[0] or get_key(playerlist, j)[0] == traitor[0]:
            continue
        k = get_key(playerlist, j)[0]
        character = identity[0]
        if character == "反贼":
            if rebel_count <= 0 and loyal_count > 0:
                character = "忠臣"
            rebel_count -= 1
        if character == "忠臣":
            if rebel_count <= 0 and loyal_count > 0:
                character = "反贼"
            rebel_count -= 1
        playeridentity[k] = character
        playerblock[k] = False
        await bot.call_api("send_private_msg", user_id=k, message="您的身份为%s, 请注意保存! "%(character))
    block_3 = True
    block_2 = False
    await choose_identity.send("身份分发结束, 下面请所有玩家选择武将")
    i = 0
    return
    
@choose_general.handle()
async def cg(bot:Bot, event:GroupMessageEvent):
    global playerlist,i,playergeneral,playerlives,block_2,generals,block_4
    usr_id = str(event.user_id)
    group_id = str(event.group_id)
    if group_id != "441320920":
        return
    if block_2:
        return
    msg = str(event.message)
    if msg in list(generals.keys()):
        if usr_id in (list(playergeneral.keys())):
            await choose_general.send(Message("[CQ:at,qq=%s]您已经选过了, 休息一下吧qwq"%(usr_id)))
            return
        if msg in list(playergeneral.values()):
            await choose_general.send(Message("[CQ:at,qq=%s][%s]已经选择过了qwq, 换一个吧~")%(usr_id, msg))
        playergeneral[usr_id] = msg
        playerlives[usr_id] = generals[msg]
        playerlifemax[usr_id] = generals[msg]
        await choose_general.send(Message("[CQ:at,qq=%s]您选择了[%s], 当前共有 %s 点体力"%(usr_id, playergeneral[usr_id], playerlives[usr_id])))
    elif usr_id not in list(playerlist.keys()):
        return
    else:
        await choose_general.send(Message("[CQ:at,qq=%s]似乎没有这个角色呢..."%(usr_id)))
        return
    i += 1    
    if len(list(playerlist.keys())) == i:
        await choose_general.send("武将选择完毕, 游戏开始~")
        if i < 5:
            playerblock[get_key(playerlist, 1)[0]] = True
            for j in (playerlist.keys()):
                if j == get_key(playerlist, 1)[0]:
                    continue
                playerblock[j] = False
        block_2 = True 
        block_4 = False     

@call_up.handle()
async def ca(bot: Bot, event:GroupMessageEvent):
    global playerlist,i,block
    print(i)
    usr_id = str(event.user_id)
    group_id = str(event.group_id)
    if group_id != "441320920":
        return
    if block:
        await call_up.finish(Message("[CQ:at,qq=%s]游戏已经开始了qwq, 请您等待下一场吧awa"%(usr_id)))
    if usr_id in list(playerlist.keys()):
        await call_up.finish(Message("[CQ:at,qq=%s]您似乎加入过了..."%(usr_id)))
    if len(list(playerlist.keys())) > 8:
        await call_up.finish(Message("[CQ:at,qq=%s]很遗憾, 当前场上预备人数已超过八人, 无法接着加入了, 我们等下一局吧awa"%(usr_id)))
    i += 1
    print(i)
    playerlist[usr_id] = i
    playerequipment[usr_id] = [] 
    await call_up.send(Message("[CQ:at,qq=%s]加入成功awa, 您是第%s位加入的(第一位加入的才可以命令开始游戏哟)"%(usr_id, i)))

@start.handle()
async def st(bot:Bot, event:GroupMessageEvent):
    global playerlist,block,block_2,i,block_3
    usr_id = str(event.user_id)
    group_id = str(event.group_id)
    if group_id != "441320920":
        return
    if usr_id not in list(playerlist.keys()):
        await start.finish(Message("[CQ:at,qq=%s]您还没有进入房间呢qwq"%(usr_id)))
    if playerlist[usr_id] == 1:
        if block:
            await start.finish(Message("[CQ:at,qq=%s]已经开启过了qwq, 赶紧开玩吧"%(usr_id)))
        else:
            if len(list(playerlist.keys())) < 5:
                if len(list(playerlist.keys())) == 1:
                    await start.send("当前人数为1人, 单人无法开始三国杀游戏")
                    return
                await start.send("当前人数小于5人, 将跳过身份分发, 直接开始选择武将")
                i = 0
                block_2 = False
                return
            if len(list(playerlist.keys())) == 7:
                await start.finish("当前在场人数为7人, 7人因特殊原因无法开始三国杀游戏, 您可以选择让人退出或让其他人加入awa")
            block = True
            i = 0
            await start.send("游戏开始, 现在开始分发身份")
            block_3 = False
    else:
        await start.finish(Message("[CQ:at,qq=%s]您似乎不是第1位加入的, 第1位加入的人员才可以命令开始哦"%(usr_id)))

@logout.handle()
async def lg(bot: Bot, event:GroupMessageEvent):
    global playerlist,i,block
    usr_id = str(event.user_id)
    group_id = str(event.group_id)
    if group_id != "441320920":
        return
    if not block:
        if usr_id in list(playerlist.keys()):
            i -= 1
            playerlist.pop(usr_id)
            await logout.send(Message("[CQ:at,qq=%s]退出成功awa"%(usr_id)))
        else:
            await logout.send(Message("[CQ:at,qq=%s]您似乎没有加入三国杀, 怎么退出呢? "%(usr_id)))
    if block:
        await logout.send(Message("[CQ:at,qq=%s]很抱歉, 游戏已经开始, 现在主公才可以责令直接关闭三国杀呢qwq"%(usr_id)))

@stop.handle()
async def st(bot: Bot, event:GroupMessageEvent):
    global dieplayers,equipment,playerequipment
    global block, block_2, block_3, block_4, block_5, playerlist, playercards, playerlives, playerblock, playergeneral, playeridentity, identity, generals, all_cards, i
    usr_id = str(event.user_id)
    group_id = str(event.group_id)
    if group_id != "441320920":
        return
    block = False
    block_2 = True
    block_3 = True
    block_4 = True
    block_5 = True
    i = 0
    playerlist = {}
    playergeneral = {}
    playerlives = {}
    playercards = {}
    playeridentity = {}
    playerblock = {}
    playerequipment = {}
    dieplayers = []
    identity = ["主公", "内奸", "反贼", "忠臣"]
    generals = {"硝酸钠":4, "小ming":4, "Miku":3, "瑄瑄啊":2, "阿云":4, "pui":5, "群主姐姐":4, "高铁":4, "U235":4, "星雨":4, "大白":4, 
    "南周白明":4, "nb":4, "标·硝酸钠":4, "神·硝酸钠":4}
    card_list = ["黑桃7 杀", "黑桃8 杀", "黑桃Ⅷ 杀", "黑桃Ⅸ 杀", "黑桃9 杀", "黑桃X 杀", "黑桃10 杀", "梅花 2 杀", "梅花3 杀", "梅花4 杀",
    "梅花5 杀", "梅花6 杀", "梅花7 杀", "梅花8 杀", "梅花Ⅷ 杀", "梅花9 杀", "梅花Ⅸ 杀", "梅花10 杀", "梅花X 杀", "梅花J 杀", "梅花11 杀", "红桃10 杀",
    "红桃X 杀", "红桃J 杀", "方块6 杀", "方块7 杀", "方块8 杀", "方块9 杀", "方块10 杀", "方块K 杀", "红桃4 火杀", "红桃7 火杀", "红桃10 火杀", "方块4 火杀",
    "方块5 火杀", "黑桃4 雷杀", "黑桃5 雷杀", "黑桃6 雷杀", "黑桃7 雷杀", "黑桃8 雷杀", "梅花5 雷杀", "梅花6 雷杀", "梅花7 雷杀", "梅花8 雷杀", "黑桃3 过河拆桥",
    "黑桃4 过河拆桥","黑桃Q 过河拆桥", "梅花3 过河拆桥", "梅花4 过河拆桥","红桃Q 过河拆桥", "黑桃3 顺手牵羊", "黑桃4 顺手牵羊", "黑桃J 顺手牵羊", "方块3 顺手牵羊",
    "方块4 顺手牵羊", "黑桃A 决斗", "梅花A 决斗", "方块A 决斗", "梅花Q 借刀杀人", "梅花K 借刀杀人", "红桃7 无中生有", "红桃8 无中生有", "红桃9 无中生有", 
    "红桃J 无中生有", "黑桃J 无懈可击", "黑桃K 无懈可击", "梅花Q 无懈可击", "梅花K 无懈可击", "红桃A 无懈可击", "红桃K 无懈可击", "方块Q 无懈可击", "黑桃J 铁索连环", 
    "黑桃Q 铁索连环", "梅花10 铁索连环", "梅花J 铁索连环","梅花Q 铁索连环", "梅花K 铁索连环", "红桃2 火攻", "红桃3 火攻", "方块Q 火攻", "红桃A 万箭齐发", "黑桃7 南蛮入侵",
    "黑桃K 南蛮入侵", "梅花7 南蛮入侵", "红桃A 桃园结义", "红桃3 五谷丰登", "红桃4 五谷丰登", "黑桃A 闪电","红桃Q 闪电", "黑桃6 乐不思蜀", "红桃6 乐不思蜀",
    "梅花6 乐不思蜀","黑桃10 兵粮寸断","梅花4 兵粮寸断","梅花A 诸葛连弩","方片A 诸葛连弩","黑桃6 青釭剑","黑桃2 雌雄双股剑","黑桃2 寒冰剑","黑桃A 古锭刀","方块5 贯石斧","黑桃5 青龙偃月刀","黑桃Q 丈八蛇矛",
    "方块Q 方天画戟","方块A 朱雀羽扇","红桃A 麒麟弓","方块Q 银月枪","黑桃2 八卦阵","梅花2 八卦阵","梅花2 仁王盾","黑桃2 藤甲","梅花2 藤甲","梅花A 白银狮子",
    "黑桃5 +1马","红桃K +1马","方块K +1马","梅花5 +1马","黑桃K -1马","红桃5 -1马","方块K -1马","方块5 木牛流马"]
    equipment=["梅花A 诸葛连弩","方片A 诸葛连弩","黑桃6 青釭剑","黑桃2 雌雄双股剑","黑桃2 寒冰剑","黑桃A 古锭刀","方块5 贯石斧","黑桃5 青龙偃月刀","黑桃Q 丈八蛇矛",
    "方块Q 方天画戟","方块A 朱雀羽扇","红桃A 麒麟弓","方块Q 银月枪","黑桃2 八卦阵","梅花2 八卦阵","梅花2 仁王盾","黑桃2 藤甲","梅花2 藤甲","梅花A 白银狮子",
    "黑桃5 +1马","红桃K +1马","方块K +1马","梅花5 +1马","黑桃K -1马","红桃5 -1马","方块K -1马","方块5 木牛流马"]
    all_cards = len(card_list)
    await stop.send("重置成功")