# -*- coding: utf-8 -*-
import scrapy
import json
from demo.items import DemoItem


class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['lianjia.com']
    start_urls = ['https://dl.lianjia.com/ershoufang/']

    def parse(self, response):
        page_data = response.css('div.page-box::attr(page-data)').extract_first()
        page_data = json.loads(page_data)
        total_page = page_data['totalPage']
        page_url_pattern = response.css('div.page-box::attr(page-url)').extract_first()
        for sel in response.xpath('//ul[@class="sellListContent"]//li[@class="clear LOGCLICKDATA"]'):
            item = DemoItem()
            title = sel.xpath('div[@class="info clear"]/div[@class="title"]/a/text()').extract()
            houseArea = sel.xpath('div[@class="info clear"]/div[@class="address"]/div[@class="houseInfo"]/a/text()') \
                .extract()
            houseInfo = sel.xpath('div[@class="info clear"]/div[@class="address"]/div[@class="houseInfo"]/text()') \
                .extract()
            totalPrice = sel.xpath('div[@class="info clear"]/div[@class="priceInfo"]/'
                               'div[@class="totalPrice"]/span/text()').extract()
            unitPrice = sel.xpath('div[@class="info clear"]/div[@class="priceInfo"]/'
                              'div[@class="unitPrice"]/span/text()').extract()
            item["title"] = title
            item["houseArea"] = houseArea
            item["houseInfo"] = houseInfo
            item["totalPrice"] = totalPrice
            item["unitPrice"] = unitPrice
            yield item

        for page in range(0, total_page):
            yield response.follow(page_url_pattern.replace('{page}', str(page)))




