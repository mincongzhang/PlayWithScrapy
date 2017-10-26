# -*- coding: utf-8 -*-
from glob import glob
import os
import scrapy

class ToScrapeSpiderYahooSummary(scrapy.Spider):
    name = "yahoo_summary"
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
        url_mid     = "/?p="
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
        filename = self.out_path+response.meta['ticker']+"_summary.csv"

        #Check filesize, if not empty, skip
        if os.path.isfile(filename) and os.path.getsize(filename) > 0:
            return

        out_file = open(filename,"w")

        success = False
        success |= self.parse_tag(out_file,response,"Market cap")
        success |= self.parse_tag(out_file,response,"Beta")
        success |= self.parse_tag(out_file,response,"PE ratio (TTM)")
        success |= self.parse_tag(out_file,response,"EPS (TTM)")
        success |= self.parse_tag(out_file,response,"Earnings date")
        success |= self.parse_tag(out_file,response,"Forward Dividend & Yield")
        success |= self.parse_tag(out_file,response,"Ex-dividend date")
        success |= self.parse_tag(out_file,response,"1y target est")

        if success:
            out_file.write(response.url+"\n")

        out_file.close()

        #Remove if empty
        if os.path.getsize(filename) == 0:
            os.remove(filename)

    #############################################################

    def parse_tag(self, out_file, response, tag_name):

        # Parse tag
        path_name = "//td/span[contains(text(),'"+tag_name+"')]"
        head  = response.xpath(path_name)
        next = head.xpath("./../following-sibling::td")
        tag = next.xpath("./span/text()")
        tag_value = tag.extract_first()

        if not tag_value:
            return False

        print(tag_name+self.field_delim+tag_value)
        out_file.write(tag_name+self.field_delim+tag_value)
        out_file.write("\n")

        return True

