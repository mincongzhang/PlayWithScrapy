# -*- coding: utf-8 -*-

from selenium import webdriver
from time import sleep

driver = webdriver.PhantomJS()
driver.set_window_size(800, 600) # set the window size that you need
driver.get('https://uk.finance.yahoo.com/quote/AAPL?p=AAPL')
driver.save_screenshot('out.png')



