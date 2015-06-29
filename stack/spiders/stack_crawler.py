# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class StackCrawlerSpider(CrawlSpider):
    name = 'stack_crawler'
    allowed_domains = ['stackoverflow.com']
    start_urls = [
        'http://stackoverflow.com/questions?sort=frequent'
    ]

    rules = (
        Rule(LinkExtractor(allow=r'questions\?page=[0-9]&sort=frequent'),
             callback='parse_item', follow=True),
    )

    def parse(self, response):
        for href in response.xpath('//div[@class="question-summary"]'):
            url = response.urljoin(href.xpath('div/h3/a/@href').extract()[0])
            yield scrapy.Request(url, callback=self.parse_item)

    def parse_item(self, response):
        yield {
            'title': response.xpath('//h1/a/text()').extract()[0],
            'url': response.url,
            'tags': response.xpath('//a[@class="post-tag"]/text()').extract(),
            'status': {
                'votes': response.xpath(
                    '//div[@class="vote"]/span/text()').extract()[0],
                'favorite_count': response.xpath(
                    '//div[@class="favoritecount"]/b/text()').extract()[0],
                'answers': response.xpath(
                    '//span[@itemprop="answerCount"]/text()').extract()[0],
                'views': response.xpath(
                    '//td/p[@class="label-key"]/b/text()').extract()[1][:-6],
            },
        }
