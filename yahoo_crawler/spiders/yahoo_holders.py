# -*- coding: utf-8 -*-
from glob import glob
import os
import scrapy

class ToScrapeSpiderYahooHolders(scrapy.Spider):
    name = "yahoo_holders"
    out_path = "/home/user/mizhang/hackathon/crawler/out/"
    field_delim = "|"

    def start_requests(self):
        # Load tickers
        ticker_file = open(self.out_path+"tickers.txt","r")
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
            request.meta['max_retry_times'] = 10
            request.meta['download_timeout'] = 10
            request.meta['download_latency'] = 10
            yield request


    def parse(self, response):
        filename = self.out_path+response.meta['ticker']+"_holders.csv"

        #Check filesize, if not empty, skip
        if os.path.isfile(filename) and os.path.getsize(filename) > 0:
            return

        out_file = open(filename,"w")

        success = False
        success |= self.parse_table(out_file,response,"Top mutual fund holders")
        success |= self.parse_table(out_file,response,"Top institutional holders")
        if success:
            out_file.write(response.url+"\n")

        out_file.close()

        #Remove if empty
        if os.path.getsize(filename) == 0:
            os.remove(filename)


    #############################################################

    def parse_table(self, out_file, response, table_name):

        # Parse table
        path_name = "//h3/span[contains(text(),'"+table_name+"')]"
        head  = response.xpath(path_name)
        table = head.xpath("./../following-sibling::table")
        rows  = table.xpath("./tbody/tr")

        # Check empty
        if not rows:
            return False

        # Write to file
        out_file.write(table_name+"\n")
        # Write fields name
        fields = ["Holder", "Shares", "Date reported", "% out","Value"]
        str_fields = self.field_delim.join(fields)
        out_file.write(str_fields+"\n")

        for row in rows:
            #all text under td
            text = row.xpath(".//td/text()").extract()

            #extract date_reported at position 2, and insert to text
            date_reported = row.xpath(".//td/span/text()").extract_first()
            text.insert(2,date_reported)

            #convert elements in list to string
            str_elems = []
            for elem in text:
                str_elems.append(elem);

            #split with delim
            one_line = self.field_delim.join(str_elems)
            print(one_line)
            out_file.write(one_line+"\n")

        out_file.write("\n")
        return True
