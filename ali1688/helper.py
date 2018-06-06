import math
import re

import requests


def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").content

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

def changeTime(allTime):
    day = 24 * 60 * 60
    hour = 60 * 60
    min = 60
    if allTime < 60:
        return "%d sec" % math.ceil(allTime)
    elif allTime > day:
        days = divmod(allTime, day)
        return "%d days, %s" % (int(days[0]),  changeTime(days[1]))
    elif allTime > hour:
        hours = divmod(allTime, hour)
        return '%d hours, %s' % (int(hours[0]),  changeTime(hours[1]))
    else:
        mins = divmod(allTime, min)
        return "%d mins, %d sec" % (int(mins[0]), math.ceil(mins[1]))

def str_replace_new(str):
    reg = r'[促销|wish|ebay|速卖通|敦煌|亚马逊|跨境|专供||欧美|夜店|性感|2017|2018|货源|爆款|不支持退货| ！|洲站|特价商品，不支持退换！介意勿拍！|+|，| ]'
    pattern = re.compile(reg, re.IGNORECASE)
    out = re.sub(pattern, '', str)
    return out
