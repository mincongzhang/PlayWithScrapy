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
        # Create an empty file
        if os.path.exists(self.filename):
            os.remove(self.filename)

        # Load tickers
        ticker_file = open("tickers.txt","r")
        tickers = []
        for line in ticker_file:
            tickers.append(line.strip())
        ticker_file.close();

        # Send url to parse
        url_prefix  = "https://uk.finance.yahoo.com/quote/"
        url_mid     = "/holders?p="
        for ticker in tickers:
            url = url_prefix+ticker+url_mid+ticker
            request = scrapy.Request(url=url, callback=self.parse)
            request.meta['ticker'] = ticker
            request.meta['dont_redirect'] = 1
            yield request


    def parse(self, response):
        out_file = open(self.filename,"a")
        out_file.write(response.meta['ticker']+"\n")
        out_file.write(response.url+"\n")

        self.parse_table(out_file,response,"Top mutual fund holders")
        self.parse_table(out_file,response,"Top institutional holders")

        out_file.close()


    #############################################################

    def parse_table(self,out_file, response, table_name):
        out_file.write(table_name+"\n")

        # Write fields name
        fields = ["Holder", "Shares", "Date reported", "% out","Value"]
        str_fields = self.field_delim.join([str(elem) for elem in fields])
        out_file.write(str_fields+"\n")

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
            out_file.write(one_line+"\n")
        out_file.write("\n")

