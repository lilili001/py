import math
import re


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
    reg = r'[促销|wish|ebay|速卖通|敦煌|亚马逊|跨境|专供||欧美|夜店|性感|2017|2018|货源|爆款]'
    pattern = re.compile(reg, re.IGNORECASE)
    out = re.sub(pattern, '', str)
    return out