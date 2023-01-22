from PIL import Image
import numpy as np
import sys


class Script:
    def __init__(self, args):
        self.args = args
        self.image = None
        self.mid_value = 127

    def check_img(self): #check if image file is present and valid
        if len(self.args) > 1:
            if self.args[1] != "-h":
                try:
                    self.image = Image.open(self.args[1])
                except:
                    self.error('invalid image')
            elif self.args[1] == "-h":
                self.help()
        else:
            self.error('no image provided')

    def help(self):
        print("Usage: python image_to_braille.py <image>")
        exit()

    def convert(self):
        self.check_img()
        self.image = self.image.convert("L")    #convert image to grayscale
        height = int(self.image.size[1]/4)      #get dimensions of the amount of braille characters needed
        width = int(self.image.size[0]/2)

        braille_characters = np.array([chr(0x2800 + i) for i in range(256)])    #populate array with all braille characters
        imgarr = np.asarray(self.image)

        braille_img = ""
        for r in range(height):
            for c in range(width):
                char = []
                for i in range(4):
                    for j in range(2):
                        try:
                            char.append(imgarr[i+r*4][j+c*2])   #split image array in blocks of 2x4 pixels
                        except:
                            self.error()
                val = 0
                for i in range(len(char)):
                    if char[i] < self.mid_value:    #decide which pixels in a block are above the mid_value and generate a binary
                        val += 2**i                 #number that correspondents with a braille character
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


    def error(self, msg="error occured"):
        print('Error: ' + msg)
        self.help()



if __name__ == '__main__':
    img_to_braille = Script(sys.argv)
    img_to_braille.convert()