# -*- coding: utf-8 -*-
from glob import glob
import os

import scrapy

#https://stackoverflow.com/questions/41472582/first-time-using-scrapy-trying-to-crawl-a-set-of-tables

class ToScrapeSpiderYahooHolders(scrapy.Spider):
    name = 'yahoo_holders'
    filename = name+".txt"
    field_delim = "|"

    def start_requests(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

        urls = [
            'https://uk.finance.yahoo.com/quote/AAPL/holders?p=AAPL',
            'https://uk.finance.yahoo.com/quote/BABA/holders?p=BABA',
        ]

        for url in urls:
           yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        file = open(self.filename,"a")
        file.write(response.url+"\n\n")

        self.parse_table(file,response,"Top mutual fund holders")
        self.parse_table(file,response,"Top institutional holders")

        file.close()


    #############################################################

    def parse_table(self, file, response, table_name):
        file.write(table_name+"\n")

        # Write fields name
        fields = ["Holder", "Shares", "Date reported", "% out","Value"]
        str_fields = self.field_delim.join([str(elem) for elem in fields])
        file.write(str_fields+"\n")

        # Parse table
        path_name = "//h3/span[contains(text(),'"+table_name+"')]"
        head  = response.xpath(path_name)
        table = head.xpath("./../following-sibling::table")
        rows  = table.xpath("./tbody/tr")

        for row in rows:
            #all text under td
            text = row.xpath(".//td/text()").extract()

            #extract date_reported at position 2, and insert to text
            date_reported = row.xpath(".//td/span/text()").extract_first()
            text.insert(2,date_reported)

            #convert elements in list to string, and split by "|"
            one_line = self.field_delim.join([str(elem) for elem in text])
            print(one_line)
            file.write(one_line+"\n")
        file.write("\n")

