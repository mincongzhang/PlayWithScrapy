# -*- coding: utf-8 -*-
from glob import glob
import os
import scrapy

class ToScrapeSpiderYahooStats(scrapy.Spider):
    name = 'yahoo_stats'
    field_delim = "|"

    def start_requests(self):
        # Load tickers
        ticker_file = open("tickers.txt","r")
        tickers = []
        for line in ticker_file:
            tickers.append(line.strip())
        ticker_file.close();

        # Send url to parse
        url_prefix  = "https://uk.finance.yahoo.com/quote/"
        url_mid     = "/key-statistics?p="
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
        pass
