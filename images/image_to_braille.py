from PIL import Image
import numpy as np
import sys

class Script:
    def __init__(self, args):
        self.args = args
        self.image = None
        self.braille_characters = ""
        self.mid_value = 127
        for i in range(0,256):
            self.braille_characters += chr(0x2800 + i)

    def check_img(self):
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
        self.image = self.image.convert("L")
        height = int(self.image.size[1]/4)
        width = int(self.image.size[0]/2)

        imgarr = np.asarray(self.image)

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
                for i in range(len(char)):
                    if char[i] < self.mid_value:
                        val += 2**i
                try:
                    if val != 0:
                        braille_img += self.braille_characters[val]
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