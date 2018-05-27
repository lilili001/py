import threading,_thread,time


def print_time(thread_name, counter, delay):
    while counter:
        time.sleep(delay)
        print("==print_time()=====%s %s========" % (thread_name,time.ctime(time.time())) )
        counter -=1

class MyThread(threading.Thread):
    def __init__(self,thread_id,name,counter):
        super(MyThread, self).__init__()  # 调用父类的构造函数
        self.thread_id = thread_id
        self.name = name
        self.counter = counter

    def run(self):
        print('Starting thread  [%s] : (%s) '% (self.name, time.ctime(time.time()))  )
        print_time(self.name, self.counter, 5)
        print('Exsiting thread  [%s] : (%s) '% (self.name, time.ctime(time.time())) )


def main():
    #创建新的线程
    t1 = MyThread(1,'thread-1',1)
    t2 = MyThread(2,'thread-2',5)

    t1.start()
    t1.join()

    t2.start()
    t2.join()

if __name__ == "__main__":
    main()