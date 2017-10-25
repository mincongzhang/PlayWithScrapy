from PIL import Image

img = Image.open("AAPL.png")
#left, upper, right, lower
area = (20, 435, 650, 675)
img.crop(area).save("result.png")
