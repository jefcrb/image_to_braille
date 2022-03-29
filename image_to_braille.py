from PIL import Image
import numpy as np
import sys

def check_img(args):
    if len(args) > 1:
        if args[1] != "-h":
            try:
                image = Image.open(args[1])
            except:
                print("This is not a valid image")
                help()
        elif args[1] == "-h":
            help()
    else:
        print("No image was provided")
        help()

    return image


def help():
    print("Usage: python image_to_braille.py <image>")
    exit()

image = check_img(sys.argv)

braille_characters = ""
for i in range(0,256):
    braille_characters += chr(0x2800 + i)

image = image.convert("L")

height = int(image.size[1]/4)
width = int(image.size[0]/2)

imgarr = np.asarray(image)

braille_img = ""
for r in range(height):
    for c in range(width):
        char = []
        for i in range(4):
            for j in range(2):
                try:
                    char.append(imgarr[i+r*4][j+c*2])
                except:
                    print("error")
        val = 0
        if char[0] < 127:
            val += 1
        if char[1] < 127:
            val += 8
        if char[2] < 127:
            val += 2
        if char[3] < 127:
            val += 16
        if char[4] < 127:
            val += 4
        if char[5] < 127:
            val += 32
        if char[6] < 127:
            val += 64
        if char[7] < 127:
            val += 128
        try:
            if val != 0:
                braille_img += braille_characters[val]
            else:
                braille_img += " "
        except:
            print(val)
    braille_img += "\n"

f = open("image_to_braille.txt", "a+", encoding="utf-8")
f.truncate(0)
f.write(braille_img)
f.close()

print("Program finished successfully")