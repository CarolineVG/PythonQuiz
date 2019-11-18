from tkinter import Canvas, Tk, Label, Button
from PIL import Image, ImageDraw, ImageTk
from tkinter.constants import *


class GradientFrame(Canvas):

    def __init__(self, master):
        Canvas.__init__(self, master)

        self.setBackgroundColor2()
        #self.setBackgroundColor((255, 179, 107), (255, 103, 91), 800)


        # image
        img = ImageTk.PhotoImage(Image.open("../trophy.png"))
        self.create_image(10, 10, anchor=NW, image=img)

    def setBackgroundColor(self, color1, color2, height):
        color1 = color1
        color2 = color2

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

        #label1 = Label(self, text='Home', fg='black', font=('arial', 24, 'bold')).pack(side="top", fill="x", pady=5)



    def setBackgroundColor2(self):
        self.configure(bg='#FE715B')



if __name__ == "__main__":

    root = Tk()

    GradientFrame(root).pack(fill=X)

    root.mainloop()
