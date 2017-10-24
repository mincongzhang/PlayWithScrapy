from selenium import webdriver


driver = webdriver.PhantomJS()
driver.set_window_size(1024, 768) # set the window size that you need
driver.get('https://uk.finance.yahoo.com/chart/AAPL')
driver.save_screenshot('out.png')
