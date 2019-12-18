# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.http import Request
from ..items import CommentsCrawlerItem
from ..pipelines import MongoDBPipeline
from ..utils.get_threadid import threadid_list
import json
from scrapy.shell import inspect_response

class CommentsSpider(Spider):
    name = 'comments'
    base_url = "http://music.163.com/api/v1/resource/comments/%s"
    start_urls = [base_url % threadid for threadid in threadid_list]

    pipeline = set([
        MongoDBPipeline,
    ])

    def parse(self, response):
        comments = json.loads(response.body)
        for item in comments['hotComments']:
            hotComments_item = CommentsCrawlerItem()
            songId = response.url.replace(
                'http://music.163.com/api/v1/resource/comments/R_SO_4_',
                ''
            )
            hotComments_item['songId'] = songId
            hotComments_item['commentId'] = item['commentId']
            hotComments_item['content'] = item['content']
            hotComments_item['likedCount'] = item['likedCount']
            hotComments_item['time'] = item['time']
            hotComments_item['nickname'] = item['user']['nickname']
            hotComments_item['userId'] = item['user']['userId']
            hotComments_item['avatarUrl'] = item['user']['avatarUrl']

            yield hotComments_item
