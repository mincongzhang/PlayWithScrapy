import os
# Load tickers
ticker_file = open("tickers.txt","r")
tickers = []
for line in ticker_file:
    tickers.append(line.strip())
ticker_file.close();

for ticker in tickers:
    system_cmd = "phantomjs js_screenshot.js " + ticker
    print("running system cmd: ["+system_cmd+"]")
    os.system(system_cmd)
