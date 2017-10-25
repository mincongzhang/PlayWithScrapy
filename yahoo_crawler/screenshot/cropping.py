from PIL import Image

img = Image.open("out.png")
#left, upper, right, lower
area = (20, 520, 650, 760)
img.crop(area).save("result.png")
