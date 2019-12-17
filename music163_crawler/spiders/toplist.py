# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.http import Request
from ..items import ToplistCrawlerItem
from ..pipelines import RedisPipeline
from ..utils.ranking_dict import rank_id
from lxml import etree
import json
from scrapy.shell import inspect_response


class ToplistSpider(Spider):
    name = 'toplist'
    base_url = "https://music.163.com/discover/toplist?id=%s"
    start_urls = [base_url % id for id in rank_id.values()]

    pipeline = set([
        RedisPipeline,
    ])

    def parse(self, response):
        html = etree.HTML(response.body)
        songs_text = html.xpath('//textarea/text()')
        songs_json = json.loads(songs_text[0])
        for item in songs_json:
            songs_item = ToplistCrawlerItem()
            songs_item['songName'] = item['album']['name']
            songs_item['commentThreadId'] = item['commentThreadId']

            yield songs_item

