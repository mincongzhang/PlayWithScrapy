# -*- coding: utf-8 -*-
import scrapy


class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'toscrape-xpath'
    start_urls = [
        'https://uk.finance.yahoo.com/quote/AAPL/holders?p=AAPL',
        'https://uk.finance.yahoo.com/quote/BABA/holders?p=BABA',
    ]
    for url in urls:
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        rows = response.xpath("//tr")
        for row in rows:
            text = row.xpath(".//td/text()").extract_first()
            yield {
                'text': text
            }
