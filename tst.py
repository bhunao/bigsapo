import PIL
import sys
from PIL import Image
import os, sys
path = sys.argv[1]

perc = int(sys.argv[2])/100 if len(sys.argv) >= 3 else 0.15
dirs = os.listdir( path )
print(sys.argv)
print(f"folder: '{dirs}'")
print(f"percentage: '{perc}'")
def resize():
    for item in dirs:
        if os.path.isfile(path+item):
            img = Image.open(path+item)
            w, h = img.size
            w = int(w*perc)
            h = int(h*perc)
            print(w, h)
            f, e = os.path.splitext(path+item)
            img = img.resize((w, h), Image.ANTIALIAS)
            img.save(f + '.png') 
resize()

