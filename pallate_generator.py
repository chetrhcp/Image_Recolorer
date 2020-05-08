from PIL import Image, ImageFilter, ImageColor
import sys
import random, math

color = {
    "blue": "#0000ff",
    "red": "#ff0000",
    "green":"#00ff00",
    "yellow":"#ffff00",
    "magenta":"#ff00ff",
    "black":"#000000",
    "brown":"#996600"
}

pallate = []
partitions = []
imageFile = sys.argv[1]
im = Image.open("images/"+imageFile)
l = int(im.size[0])
w = int(im.size[1])
if len(sys.argv) < 4:
    # if nothing assume random
    for i in range(0, int(sys.argv[2])):
        rl = random.randint(0, l)
        rw = random.randint(0, w)
        point = rl, rw
        pallate.append("#%02x%02x%02x" % im.getpixel(point))
elif sys.argv[3] == "kmean++":
    rl = random.randint(0, l)
    rw = random.randint(0, w)
    point = rl, rw
    pallate.append("#%02x%02x%02x" % im.getpixel(point))


    for i in range(1, int(sys.argv[2])):
        max_dif = -1
        best_seed_pixel = 0,0,0
        for x in range(0, l):
            for y in range(0, w):
                min_dif = -1
                min_pixel = 0,0,0
                for z in range(0, len(pallate)):
                    point2 = x, y
                    seed_pixel = im.getpixel(point2)
                    previous = ImageColor.getrgb(pallate[z])
                    seed_r = abs(seed_pixel[0] - previous[0])
                    seed_g = abs(seed_pixel[1] - previous[1])
                    seed_b = abs(seed_pixel[2] - previous[2])
                    dif = math.sqrt(seed_r * seed_r + seed_g * seed_g + seed_b * seed_b)
                    if dif < min_dif or min_dif == -1:
                        min_dif = dif
                        min_pixel = seed_pixel
                if min_dif > max_dif or max_dif == -1:
                    max_dif = min_dif
                    best_seed_pixel = min_pixel
        pixel = "#%02x%02x%02x" % best_seed_pixel
        pallate.append(pixel)

elif sys.argv[3] == "manual":
    reader = open("pallates/" + sys.argv[4], "r")
    pallate = reader.read().split("\n")



for i in range(0, len(pallate)):
    partitions.append([])

pixels = list(im.getdata())
for x in range(0, 5):
    print("pass: " + str(x+1))
    print(pallate)
    for pixel in pixels:
        rgb = pixel
        min_difference = -1
        min_index = 0
        for i in range(0, len(pallate)):
            pallate_color = ImageColor.getrgb(pallate[i])
            r = abs(rgb[0] - pallate_color[0])
            g = abs(rgb[1] - pallate_color[1])
            b = abs(rgb[2] - pallate_color[2])
            dif = math.sqrt(r*r + g*g + b*b)
            if dif < min_difference or min_difference == -1:
                min_difference = dif
                min_index = i
        hexColor = "#%02x%02x%02x" % rgb
        partitions[min_index].append(hexColor)

    for i in range(0, len(partitions)):
        total = 0
        r_sum = 0
        g_sum = 0
        b_sum = 0
        for color in partitions[i]:
            rgb2 = ImageColor.getrgb(color)
            r_sum += rgb2[0]
            g_sum += rgb2[1]
            b_sum += rgb2[2]
            total += 1
        new_pallate = 0,0,0
        try:
            new_pallate = int(r_sum/total), int(g_sum/total), int(b_sum/total)
        except:
            # if a color gets no matches, randomly assign a new one
            rl = random.randint(0, l)
            rw = random.randint(0, w)
            point = rl, rw
            new_pallate = im.getpixel(point)
        print(new_pallate)
        pallate[i] = "#%02x%02x%02x" % new_pallate

writer = open("pallates/"+imageFile.split(".")[0] + ".txt", "w")
did = False
for color in pallate:
    if did:
        writer.write("\n")
    writer.write(color)
    did = True
writer.close()
size = 300, 150
im2 = Image.new(mode="RGB", size=size, color=0)
for i in range(0, size[0]):
    for j in range(0, size[1]):
        pal_point = i, j
        index = int(i /(size[0] / len(pallate)))
        im2.putpixel(pal_point, ImageColor.getrgb(pallate[index]))
im2.save("pallates/"+imageFile.split(".")[0] + ".jpg")
