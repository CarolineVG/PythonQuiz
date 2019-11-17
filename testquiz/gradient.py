# Author: Miguel Martinez Lopez
from tkinter import Canvas
from tkinter.constants import *
from PIL import Image, ImageDraw, ImageTk

class GradientFrame(Canvas):

    def __init__(self, master, color1, color2, height):
        Canvas.__init__(self, master)

        color1 = (255, 179, 107)
        color2 = (255, 103, 91)

        # color 1:
        red, green, blue = color1
        # 255 - 255 = 0 -> 0 / 800 = 0.0
        color1Red = float(color2[0] - red) / height

        # 103 - 255 = -76 -> -76 / 800 = -0.095
        color1Green = float(color2[1] - green) / height

        # 91 - 255 = 0 -> -16 / 800 = -0.02
        color1Blue = float(color2[2] - blue) / height

        # horizontal
        self.configure(height=height)

        img_height = height
        img_width = self.winfo_screenwidth()

        image = Image.new("RGB", (img_width, img_height), "#FFFFFF")
        draw = ImageDraw.Draw(image)

        # draw every row until 800 (height)
        for i in range(height):
            red = red + color1Red
            green = green + color1Green
            blue = blue + color1Blue

            # draw.rectangle(left up, left down, right down, right up)
            startPoint = 0
            rowPoint = int(float(img_height * i) / height)

            draw.rectangle((startPoint, rowPoint, img_width, rowPoint), fill=(int(red), int(green), int(blue)))

        self._gradient_photoimage = ImageTk.PhotoImage(image)
        self.create_image(0, 0, anchor=NW, image=self._gradient_photoimage)


if __name__ == "__main__":
    try:
        from Tkinter import Tk, Label
    except ImportError:
        from tkinter import Tk, Label

    root = Tk()

    GradientFrame(root, (255, 179, 107), (255, 103, 91), 800).pack(fill=X)

    root.mainloop()
