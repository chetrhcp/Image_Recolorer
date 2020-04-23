from PIL import Image, ImageFilter, ImageColor
import sys

def match_color(rgb, colors2):
    minIndex = 0
    minDiff = 800
    for i in range(0, len(colors2)):
        relative = False
        comp = rgb
        if relative:
            sub = min(rgb[0], rgb[1], rgb[2])
            ad = min(colors2[i][0], colors2[i][1], colors2[i][2])
            comp = max(min(rgb[0] - sub + ad, 255), 0), max(min(rgb[1] - sub + ad, 255), 0), max(min(rgb[2] - sub + ad, 255), 0)

        r = abs(colors2[i][0] - comp[0])
        g = abs(colors2[i][1] - comp[1])
        b = abs(colors2[i][2] - comp[2])
        num = r+g+b
        if num < minDiff:
            minIndex = i
            minDiff = num
    color2 = colors2[minIndex]
    ad2 = min(rgb[0], rgb[1], rgb[2])
    sub2 = min(color2[0], color2[1], color2[2])
    comp2 = max(min(color2[0] - sub2 + ad2, 255), 0), max(min(color2[1] - sub2 + ad2, 255), 0), max(min(color2[2] - sub2 + ad2, 255), 0)

    return comp2


def shade(rgb, shade_val):
    r = min(max(rgb[0] + shade_val, 0), 255)
    g = min(max(rgb[1] + shade_val, 0), 255)
    b = min(max(rgb[2] + shade_val, 0), 255)
    return r, g, b


def invertColor(rgb):
    r = max(255 - rgb[0], 0)
    g = max(255 - rgb[1], 0)
    b = max(255 - rgb[2], 0)
    return r, g, b

def color_inject_func(rgb, base_color, inject_color, inject_val, inject_range):
    baseRGB = ImageColor.getrgb(base_color)
    injectRGB = ImageColor.getrgb(inject_color)
    sub = min(injectRGB[0], injectRGB[1], injectRGB[2])
    r_val = baseRGB[0] - rgb[0]
    g_val = baseRGB[1] - rgb[1]
    b_val = baseRGB[2] - rgb[2]
    if(abs(r_val + g_val + b_val) < inject_range):
        r = rgb[0] + inject_val * (injectRGB[0]-sub)
        g = rgb[1] + inject_val * (injectRGB[1]-sub)
        b = rgb[2] + inject_val * (injectRGB[2]-sub)
        rgb = r, g, b
    return rgb

def blend(colors, steps):
    new_colors = []
    for i in range(0, len(colors)):
        for j in range(0, len(colors)):
            new_colors.append(colors[i])
            if i != j:
                step_r = round((colors[i][0] - colors[j][0]) / steps)
                step_g = round((colors[i][1] - colors[j][1]) / steps)
                step_b = round((colors[i][2] - colors[j][2]) / steps)
                temp_color = colors[i]
                for k in range(0, steps):
                    temp_color = temp_color[0] + step_r, temp_color[1]+step_g, temp_color[2] + step_b
                    new_colors.append(temp_color)
    return new_colors

imageFile = sys.argv[1]
recolor = False
isShade = False
invert = False
shade_val = 0
pallate = ""
colors2 = []
color_inject = False
base_color = 0
inject_color = 0
inject_val = 0
inject_range = 0
for i in range(2, len(sys.argv)):
    if sys.argv[i] == "recolor":
        recolor = True
        pallate = sys.argv[i+1]
        colors = open("pallates/" + pallate, "r").read().split("\n")
        for color in colors:
            rgb = color.split(",")
            rgb_tup = int(rgb[0]), int(rgb[1]), int(rgb[2])
            colors2.append(rgb_tup)
    elif sys.argv[i] == "shade":
        isShade = True
        shade_val = int(sys.argv[i+1])
    elif sys.argv[i] == "invert":
        invert = True
    elif sys.argv[i] == "color_inject":
        color_inject = True
        base_color = sys.argv[i+1]
        inject_color = sys.argv[i+2]
        inject_val = int(sys.argv[i+3])
        inject_range = int(sys.argv[i+4])



#colors2 = blend(colors2, 3)

im = Image.open("images/"+imageFile)
l = int(im.size[0])
w = int(im.size[1])
im2 = Image.new(mode="RGB", size=im.size, color=0)
for i in range(0, l):
    for j in range(0, w):
        point = i, j
        rgb = im.getpixel(point)
        if invert:
            rgb = invertColor(rgb)
        if isShade:
            rgb = shade(rgb, shade_val)
        if recolor:
            rgb = match_color(rgb, colors2)
        if color_inject:
            rgb = color_inject_func(rgb, base_color, inject_color, inject_val, inject_range)


        im2.putpixel(point, rgb)
tag = ""
if recolor: tag += "_" + pallate.split(".")[0]
if isShade: tag += "_shade"
if invert: tag += "_invert"
if color_inject: tag += "_color_inject"

newFileName = imageFile.split('.')[0] + tag + '.' + imageFile.split('.')[1]
print(newFileName)
im2.save("images/"+newFileName)
