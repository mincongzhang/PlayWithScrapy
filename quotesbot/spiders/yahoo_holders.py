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
        file = open(self.filename,"a")
        file.write(response.url+"\n\n")

        file.write("Top mutual fund holders \n")
        #Top mutual fund holders
        #https://stackoverflow.com/questions/39969770/scrapy-xpath-with-text-contains
        #https://stackoverflow.com/questions/19767517/how-to-select-next-node-using-scrapy
        head  = response.xpath("//h3/span[contains(text(),'Top mutual fund holders')]")
        table = head.xpath("./../following-sibling::table")
        rows  = table.xpath("./tbody/tr")
        for row in rows:
            #all text under td
            text = row.xpath(".//td/text()").extract()

            #extract date_reported at position 2, and insert to text
            date_reported = row.xpath(".//td/span/text()").extract_first()
            text.insert(2,date_reported)

            #convert elements in list to string, and split by "|"
            one_line = "|".join([str(elem) for elem in text])
            print(one_line)
            file.write(one_line+"\n")

        file.write("\n")
        file.close()



