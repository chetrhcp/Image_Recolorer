from PIL import Image
import sys

imageFile = sys.argv[1]
im = Image.open("images/"+imageFile)

palette_var = list(im.getdata())

print(palette_var)