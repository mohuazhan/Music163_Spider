# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import functools
import pymongo
import redis


def check_spider_pipeline(process_item_method):
    '''
    在单个Scrapy项目中为不同的蜘蛛使用不同的管道：
    对Pipeline对象的process_item方法使用此装饰器，
    以便它检查spider的pipeline属性，
    以确定它是否应该被执行
    '''

    @functools.wraps(process_item_method)
    def wrapper(self, item, spider):
        if self.__class__ in spider.pipeline:
            return process_item_method(self, item, spider)

        else:
            return item

    return wrapper


class Music163CrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


class RedisPipeline(object):  # 数据导出到Redis
    def __init__(self, Redis_host, Redis_port, Redis_password):
        self.Redis_host = Redis_host
        self.Redis_port = Redis_port
        self.Redis_password = Redis_password

    @classmethod
    def from_settings(cls, settings):
        return cls(
            Redis_host = settings['REDIS_HOST'],
            Redis_port = settings['REDIS_PORT'],
            Redis_password = settings['REDIS_PASSWORD']
        )

    def open_spider(self, spider):
        # 创建redis连接池
        redis_pool = redis.ConnectionPool(
            host = self.Redis_host,
            port = self.Redis_port,
            password = self.Redis_password,
            decode_responses=True
        )   # 连接redis，加上decode_responses=True，写入的键值对中的value为str类型，不加这个参数写入的则为字节类型
        self.my_redis = redis.Redis(connection_pool=redis_pool)

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.my_redis.hsetnx(
            'hash_music163_songs',
            item['songName'], 
            item['commentThreadId']
        )
        return item


class MongoDBPipeline(object):  # 数据导出到MongoDB
    def __init__(self, MongoDB_server, MongoDB_port, MongoDB_user, MongoDB_password, MongoDB_db, MongoDB_collection):
        # 连接MongoDB
        client = pymongo.MongoClient(MongoDB_server, MongoDB_port)
        database = client.admin  # 连接用户库
        database.authenticate(MongoDB_user, MongoDB_password)  # 用户认证
        database = client[MongoDB_db]  # 连接数据库
        self.collection = database[MongoDB_collection]  # 连接数据表

    @classmethod
    def from_settings(cls, settings):
        return cls(
            MongoDB_server = settings['MONGODB_SERVER'],
            MongoDB_port = settings['MONGODB_PORT'],
            MongoDB_user = settings['MONGODB_USER'],
            MongoDB_password = settings['MONGODB_PASSWORD'],
            MongoDB_db = settings['MONGODB_DB'],
            MongoDB_collection = settings['MONGODB_COLLECTION']
        )

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item