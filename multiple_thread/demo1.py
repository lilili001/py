import time,threading

def loop(count):
    print('thread [%s] is running ...' % threading.current_thread().name)
    while count > 0:
        print( 'count=%d' % count )
        count = count - 1
        time.sleep(1)

t = threading.Thread(target=loop,name="LoopThread", args=(10,) )
t.start()
t.join()