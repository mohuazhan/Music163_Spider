# -*- coding: utf-8 -*-

import redis


# 查询redis中的哈希表返回所有commentThreadId
redis_pool = redis.ConnectionPool(
    host='127.0.0.1',
    port=6379,
    password='myloveforever',
    decode_responses=True
)   # 连接redis，加上decode_responses=True，写入的键值对中的value为str类型，不加这个参数写入的则为字节类型
my_redis = redis.Redis(connection_pool=redis_pool)
threadid_list = my_redis.hgetall("hash_music163_songs").values()