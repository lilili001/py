import math
import random
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

def str_replace_en(str):
    reg = r'[+|\/|]'
    pattern = re.compile(reg, re.IGNORECASE)
    out = re.sub(pattern, '', str)
    return out

def keywords_woman_dress():
    arr = [
        'dresses',
        'maxi dresses',
        'formal dresses',
        'prom dresses',
        'evening dresses',
        'summer dresses',
        'evening gowns',
        'white dress',
        'dresses online',
        'long dresses',
        'gown',
        'cocktail dresses',
        'womens clothes',
        'homecoming dresses',
        'long sleeve dress',
        'party dresses',
        'casual dresses',
        'floral dresses',
        'ladies dress',
        'white maxi dress',
        'black dress',
        'red dress',
        'little black dress',
        "women dress",
        "women dresses size 14",
        "women dresses size 12",
        "women dress free shipping",
        "women dress plus size",
        "women dress a-line",
        "women a line dress",
        "women dress bodycon",
        "women dress boho",
        "women dress cocktail party formal evening dress",
        "women dress casual",
        "women dress cocktail",
        "women dress draped lace",
        "dress women",
        "women summer dress",
        "dress women party",
        "long dress women",
        "women dresses",
        "women dresses size 16",
        "women dresses plus size",
        "women dress formal",
        "women dress for party",
        "women dress green",
        "women dress gold",
        "women dressing gown",
        "women jumpsuit dress",
        "women dress large",
        "women dress long sleeve",
        "women dress long",
        "women dress lace",
        "women dress size m",
        "new fashion casual dress for women",
        "women dress off shoulder",
        "women dress office",
        "women dress oversize",
        "elegant women office dress",
        "women dress party",
        "women dress red",
        "women dress rockabilly",
        "women dress size 8",
        "women dress summer",
        "women dress size 6",
        "women dress size 10",
        "women dress tops",
        "women dress the party",
        "women fashion long t shirt dress",
        "women print t shirt dress",
        "women long sleeve t shirt dress",
        "women swimwear bikini cover up beach dress",
        "women dress vintage",
        "women dress v neck",
        "women v neck dress",
        "yellow v neck dresses for women",
        "women vintage dress v neck",
        "women v neck mini dress",
        "women dress xl",
        "women dress xs",
        "women dress xxl",
        "women dress xxs",
        "women dress xxxl",
        "women dressy dress",
        "women dress 16",
        "women dress 14w",
        "women dress 14",
        "women dress 10",
        "women dress 12",
        "women dress 2018",
        "women's dress suits australia",
        "women's dress suits",
        "best women's dress suits",
        "women's suits dress barn",
        "women's business dress suits",
        "women's dress suits",
        "women's dress suits canada",
        "women's dress and coat suits",
        "women's corporate dress suits",
        "cream colored women's dress suits",
        "classic women's dress suits",
        "dress code women's suits",
        "women's elegant dress suits",
        "women's evening dress suits",
        "women's dress suits for weddings",
        "women's dress suits for work",
        "women's dress pant suits for weddings",
        "women's formal dress suits",
        "women's fall dress suits",
        "women's gray dress suits",
        "women's dress and jacket suits",
        "women's dress knit suits",
        "kasper women's dress suits",
        "women's lavender dress suits",
        "women's linen dress suits",
        "women's long dress suits",
        "women's lace dress suits",
        "women's dress leather suits",
        "neiman marcus women's dress suits",
        "navy women's dress suits",
        "women's dress suits plus size",
        "women's dress suits petite",
        "women's dress pant suits",
        "women's two piece dress suits",
        "women's plus dress suits",
        "women's professional dress suits",
        "women's pink dress suits",
        "women's dress suits sale",
        "women's plus size dress suits",
        "women's dress suits with skirts",
        "women's spring dress suits",
        "women's summer dress suits",
        "women's sheath dress suits",
        "women's silk dress suits",
        "women's pant suits dress suits",
        "sears women's dress suits",
        "women's tuxedo dress suits",
        "women's tailored dress suits",
        "tahari women's dress suits",
        "women's dress suits under $50",
        "women's dress suits uk",
        "women's dress suits work",
        "www.women dress suits",
        "womens dress suits australia",
        "womens dress suits for weddings australia",
        "dress barn womens bathing suits",
        "dress barn womens pant suits",
        "womens business dress suits",
        "womens dress suits canada",
        "women dress suits",
        "classic womens dress suits",
        "lounge suits dress code women's",
        "womens evening dress suits",
        "womens dress suits for weddings",
        "womens dress suits for weddings uk",
        "womens dress pants suits for weddings",
        "womens dress suits for work",
        "womens formal dress suits",
        "womens gray dress suits",
        "women's dress and jacket work suits",
        "womens dress knit suits",
        "womens dress suits with long jackets",
        "womens lace dress suits",
        "womens dress leather suits",
        "navy blue womens dress suits",
        "womens dress suits plus size",
        "plus size womens dress pant suits",
        "petite womens dress suits",
        "womens white dress pant suits",
        "women's pant suits dress suits jacket",
        "women's petite dress pant suits",
        "women's formal dress pant suits",
        "womens dress pant suits",
        "cheap womens dress pant suits",
        "macys womens dress pant suits",
        "womens dress pant suits for weddings",
        "womens two piece dress suits",
        "womens plus dress suits",
        "womens plus size dress pant suits",
        "plus size womens dress suits",
        "professional women's dress suits",
        "womens pink dress suits",
        "womens dress suits for sale",
        "wholesale womens dress suits",
        "womens dress suits on sale",
        "womens spring dress suits",
        "dressing gowns"
    ]
    return random.sample(arr,5)