import redis
import time
pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)

# 1. sadd(name,value) 添加元素
# 2. smembers(name) 查看所有元素
# 3. scard(name) 获取name对应的集合中的元素个数
# 4. sismember(name, value) #检查value是否是name对应的集合内的元素
# 5. spop(name) #随机删除并返回指定集合的一个元素
# 6. srem(name, value)  删除集合中的某个元素

r.sadd('info','info-a')
print( r.smembers('info') )
print( r.scard('info') )
print( r.sismember('info' ,'ab' ) == False )
# print(r.spop('info'))
# # print( r.smembers('info') )