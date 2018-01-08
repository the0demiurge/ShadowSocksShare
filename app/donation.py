#!/usr/bin/env python3

# info contains (number, message, name, comment)
info = [
    (1,),
    (1.11, 'saner'),
    (10, 'HOLD ON!'),
    (5.2, '谢谢分享'),
    (5, '大佬喝冰阔落'),
    (20, '支持一下 emoji:smile'),
    (6.66, '谢谢'),
    (10,),
    (1, '感谢大佬！'),
    (10,),
    (10, '支持'),
    (1,),
    (2, '万分感谢'),
    (8.88, '再接再励。'),
    (10, '谢谢你的努力'),
    (10, '很好用，点赞！'),
    (2.33, '牛批'),
    (1,),
    (1, '等发工资再捐'),
    (5, '老铁 奉献没毛病'),
    (2, '加油兄弟'),
    (1, '好用，点赞！继续保持'),
    (8.8, '聊表心意，钱不多。'),
    (10,),
    (10, '谢谢'),
    (10, '谢谢分享'),
    (10, '资助你大兄弟加油'),
    (1, '加油哦！Ծ̮Ծ'),
    (10,),
    (5, '779595014'),
    (3, 'Respect!'),
    (0.01,),
    (5, '支持技术！谢谢技术！'),
    (5, '感谢分享'),
    (20, '感谢分享，自由无价！'),
    (20, '请再接再厉，坚持完善'),
    (2,),
    (10, '谢谢分享！'),
    (0.88,),
    (3, '感谢你免费梯子项目'),
    (8.88,),
    (5,),
    (5,),
    (10.01, '伟大，感谢与支持！'),
    (1, '用不了了(emoji哭)不过还是', '', '具体是哪方面用不了了？欢迎到我的 <a target="_blank" href="https://github.com/the0demiurge/ShadowSocksShare-OpenShift/issues">GitHub Issue 页面</a>提供反馈；<br>此外近期有计划抽空对网站升级，把不能用的帐号过滤掉：）'),
    (10, ''),
    (10, '感谢分享～加油'),
    (8, '喝瓶奶茶'),
    (5, '老大，请你吃个可乐。'),
    (10, '感谢您的ss项目'),
    (2.33, '谢谢'),
    (1, ''),
    (10, '感谢分享免费梯子'),
    (2, ''),
    (50, '', 'hsu_bicheng'),
]


def parse(data):
    if len(data) == 1:
        number, message = data[0], ''
    else:
        number, message = data[:2]
    if message:
        message = '，并留言：”{}“'.format(message)
    if len(data) >= 3:
        name = data[2]
    else:
        name = '某位没有留下名字的'

    if len(data) >= 4:
        comment = '<br>to 这位朋友：{}'.format(data[3])
    else:
        comment = ''

    return_data = '<p>{name}朋友捐献了{number}元{message}：）{comment}</p>'.format(
        name=name,
        number=number,
        message=message,
        comment=comment)
    return return_data


sum_people = len(info)
sum_money = sum(list(zip(*info))[0])
data = '\n'.join(map(parse, info))
