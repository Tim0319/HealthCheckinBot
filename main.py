#using
# https://github.com/GraiaProject/Application
import aiohttp
from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session, GroupMessage, session
from graia.application.message.chain import MessageChain
import asyncio
from graia.application.message.elements.internal import Image
from PIL import Image as IMG
from io import BytesIO
from graia.application.message.elements.internal import At, Plain
from graia.application.session import Session
from graia.application.group import Group, Member
from graia.application.message.parser.kanata import Kanata
from graia.application.message.parser.signature import FullMatch, OptionalParam, RequireParam
from graia.application.message.elements.internal import Plain
from graia.application.friend import Friend

import time

#在这里导入自己的module
import module.yuanfen as yf
import module.ocr as ocr
import module.tord as tord
import module.countreceive as countreceive


loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host="http://purecloud.top:3838", # 填入 httpapi 服务运行的地址
        authKey="qwertyuiop1234567890", # 填入 authKey
        account=2234550852, # 你的机器人的 qq 号
        websocket=True # Graia 已经可以根据所配purecloud.top置的消息接收的方式来保证消息接收部分的正常运作.
    )
)


@bcc.receiver("FriendMessage")
async def friend_message_listener(app: GraiaMiraiApplication, friend: Friend):
    await app.sendFriendMessage(friend, MessageChain.create([
        Plain("你好呀我是Mirai机器人，有事请留言，我的主人看到会回复的哦")
    ]))


# 帮助
@bcc.receiver("GroupMessage", dispatchers=[
    # 注意是 dispatcher, 不要和 headless_decorater 混起来
    Kanata([FullMatch("帮助")])
])
async def group_message_handler_help_zh(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
    saying: MessageChain
):
    print(saying.asDisplay())
    await app.sendGroupMessage(group, MessageChain.create([
        Plain(f"帮助\n发送'帮助'或者'help'来获取更多信息\n新功能\n测缘分(空格)男名(空格)女名 来测俩人缘分，快来试试吧"),
        Plain(f"\n输入真心话大冒险可以进行娱乐哦")
    ]))

# goodnight
@bcc.receiver("GroupMessage", dispatchers=[
    # 注意是 dispatcher, 不要和 headless_decorater 混起来
    Kanata([FullMatch("晚安")])
])
async def group_message_handler_goodnight(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
    saying: MessageChain
):
    print(saying.asDisplay())
    await app.sendGroupMessage(group, MessageChain.create([
        Plain(f"晚安啦，小可爱们")
    ]))


# help
@bcc.receiver("GroupMessage", dispatchers=[
    # 注意是 dispatcher, 不要和 headless_decorater 混起来
    Kanata([FullMatch("help")])
])
async def group_message_handler_help_en(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
    saying: MessageChain
):
    print(saying.asDisplay())
    await app.sendGroupMessage(group, MessageChain.create([
        Plain(f"help\nTry to send 'help' or '帮助' to grab more infomation\nnew function\ntype 测缘分(space)malename("
              f"space)girlname to get the mysterious value of the two people")
    ]))


# OCR识别并且@群成员
# 获取成员信息表
@bcc.receiver("GroupMessage")
async def group_message_handler_OCRandAT(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
    saying: MessageChain,message_info: GroupMessage
):
    #print(message_info.sender.id)
    #print(message.has(Image))

    if message_info.sender.id in [1251811859, 81414770, 961836880] and message.has(Image):
        # 保存图像
        groupList = await app.groupList()
        print("group" , message_info.sender.group.id)
        memberList = await app.memberList(message_info.sender.group.id)
        # print(groupList)
        # print(memberList)
        # print(type(memberList))
        imgs = message.get(Image)
        for i in imgs:
            async with aiohttp.ClientSession() as session:
                async with session.get(url=i.url) as resp:
                    img_content = await resp.read()
            image = IMG.open(BytesIO(img_content))
            image.save('11.png')
            # print(type(imgs))#it is a list
            content = ocr.ocr('11.png')
            print(content)
            #await app.sendGroupMessage(group, MessageChain.create([Plain(content)]))
            if "学生列表" in content or "技术支持" in content or "股份有限公司" in content:
                result_num = ocr.school_number(content)
                #print(result)
                (result,err) = ocr.at_schoolnum(result_num,memberList)
                msg = [Plain(f"Tip:保持图片学号上方无遮挡可以提高识别准确率\n请以下同学支付宝打卡\n")]
                for j in result:
                    msg.append(At(j))
                if len(err) != 0:
                    msg.append(Plain("\n群昵称中含有8位数学号便可正确识别身份啦~\n请手动@以下未匹配同学并修改其群昵称 \n"))
                    for j in err:
                        msg.append(Plain(j))
                        msg.append(Plain(f"\n"))
                await app.sendGroupMessage(group, MessageChain.create(msg))
            '''
            for i in result:
                await app.sendGroupMessage(group, MessageChain.create([
                    At(i)
                ]))
'''

# yf.yf()
# 缘分测定小程序
@bcc.receiver("GroupMessage", dispatchers=[
    # 注意是 dispatcher, 不要和 headless_decorater 混起来
    Kanata([FullMatch("测缘分"), RequireParam(name="saying")])
])
async def group_message_handler_yf(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
    saying: MessageChain
):
    print(saying.asDisplay())
    try:
        temp_yf = saying.asDisplay()[1:]
        temp_yf = temp_yf.split(" ")
        print(temp_yf)
        temp_yf = yf.yf(temp_yf[0],temp_yf[1])
        await app.sendGroupMessage(group, MessageChain.create([
            Plain(temp_yf)
        ]))
    except:
        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id),Plain("请按照规范输入，比如说\n"),Plain("测缘分 小明 小红\n"),
            Plain("空格分隔 第一个是小哥哥的名字 第二个是小姐姐的名字")
        ]))

# tord.tord()
# Truth or Dare
@bcc.receiver("GroupMessage", dispatchers=[
    # 注意是 dispatcher, 不要和 headless_decorater 混起来
    Kanata([FullMatch("真心话大冒险")])
])
async def group_message_handler_yf(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
    saying: MessageChain
):
    print("Truth or Dare")

    await app.sendGroupMessage(group, MessageChain.create([
        At(member.id),
        Plain("\n"),
        Plain(tord.tord())
    ]))




app.launch_blocking()