from fake_useragent import UserAgent

class People(object):
    color = 'yellow'

    def __init__(self,c):
        print("Init..."+c)
        self.dwell='Earth'

    def think(self):
        self.color = "black"
        print("I am a %s " % self.color)
        print("I am a thinker")

class Chinese(People):
    def __init__(self):
        People.__init__(self,'red')
    pass


if __name__ =="__main__":
    #cn = Chinese()
    # print(cn.dwell)
    # cn.think()

    ua = UserAgent()
    print(ua.random)