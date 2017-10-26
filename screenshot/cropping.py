from PIL import Image

ticker = input("Enter a ticker name: ")

img = Image.open(ticker+".png")
#left, upper, right, lower
area = (20, 435, 650, 675)
img.crop(area).save(ticker+"result.png")
