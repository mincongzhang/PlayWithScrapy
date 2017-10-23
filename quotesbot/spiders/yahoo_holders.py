# -*- coding: utf-8 -*-
import scrapy

#https://stackoverflow.com/questions/41472582/first-time-using-scrapy-trying-to-crawl-a-set-of-tables

class ToScrapeSpiderYahooHolders(scrapy.Spider):
    name = 'yahoo_holders'

    def start_requests(self):
        urls = [
            'https://uk.finance.yahoo.com/quote/AAPL/holders?p=AAPL',
            'https://uk.finance.yahoo.com/quote/BABA/holders?p=BABA',
        ]
        for url in urls:
           yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        file = open(self.name+".txt","a")
        file.write(response.url+"\n")

        #get table
        rows = response.xpath("//tr")
        for row in rows:
            text = row.xpath(".//td/text()").extract()
            print(text)
            file.write("|".join([str(x) for x in text])+"\n")

        file.close()


