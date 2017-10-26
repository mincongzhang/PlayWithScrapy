from PIL import Image
import os

# Load tickers
out_path = "/home/user/mizhang/hackathon/crawler/out/"
ticker_file = open(out_path+"tickers.txt","r")
tickers = []
for line in ticker_file:
    tickers.append(line.strip())
ticker_file.close();

for ticker in tickers:
    img_name = ticker+".png"
    print("handling ["+img_name+"]")
    if os.path.isfile(img_name):
        img = Image.open(img_name)
        #left, upper, right, lower
        area = (20, 435, 650, 675)
        img.crop(area).save(ticker+"_chart.png")
