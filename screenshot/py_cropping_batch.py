from PIL import Image
import os

# Load tickers
ticker_file = open("tickers.txt","r")
tickers = []
for line in ticker_file:
    tickers.append(line.strip())
ticker_file.close();

for ticker in tickers:
    img_name = ticker+".png"
    print("handling ["+img_name+"]")
    img = Image.open(img_name)
    #left, upper, right, lower
    area = (20, 435, 650, 675)
    img.crop(area).save(ticker+"_chart.png")
