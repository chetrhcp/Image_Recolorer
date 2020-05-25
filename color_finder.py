from PIL import Image, ImageFilter, ImageColor
import sys

imageFile = sys.argv[1]
im = Image.open("images/"+imageFile)
l = int(im.size[0])
w = int(im.size[1])
color_sum = 0, 0, 0
count = 0
for i in range(0, l):
    for j in range(0, w):
        point = i, j
        pixel = im.getpixel(point)
        color_sum = color_sum[0] + pixel[0], color_sum[1] + pixel[1], color_sum[2] + pixel[2]
        count += 1
color = int(color_sum[0] / count), int(color_sum[1]/count), int(color_sum[2]/count)
print("#%02X%02X%02X" % color)
