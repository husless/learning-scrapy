# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from stack.items import StackItem


class StackCrawlerSpider(CrawlSpider):
    name = 'stack_crawler'
    allowed_domains = ['stackoverflow.com']
    start_urls = [
        'http://stackoverflow.com/questions?pagesize=50&sort=frequent'
    ]

    rules = (
        Rule(LinkExtractor(allow=r'questions\?page=[0-9]&sort=frequent'),
             callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        questions = response.xpath('//div[@class="question-summary"]')

        for question in questions:
            item = StackItem()
            item['title'] = question.xpath(
                'div/h3/a[@class="question-hyperlink"]/text()').extract()[0]
            item['url'] = question.xpath(
                'div/h3/a[@class="question-hyperlink"]/@href').extract()[0]
            item['tags'] = question.xpath(
                 'div/div/a[@class="post-tag"]/text()').extract()
            votes = question.xpath(
                'div/div/div[@class="vote"]/div/span/strong/text()'
            ).extract()[0]
            votes = int(votes)
            answers = question.xpath(
                 'div/div/div[@class="status answered-accepted"]/strong/text()'
            ).extract()
            answers = int(answers[0]) if answers else 0
            views = question.xpath(
                'div/div[@class="views supernova"]/@title'
            ).extract()
            views = int(''.join(views[0][:-6].split(','))) if views else 0
            item['status'] = dict(votes=votes, answers=answers, views=views)
            yield item

