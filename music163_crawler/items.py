# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class ToplistCrawlerItem(Item):
    songName = Field()  # 歌曲名
    commentThreadId = Field()  # 查询评论接口对应id


class CommentsCrawlerItem(Item):
    commentId = Field()  # 评论id
    content = Field()  # 评论内容
    likedCount = Field()  # 评论获赞数
    time = Field()  # 评论时间
    nickname = Field()  # 评论者
    userId = Field()  # 评论者id