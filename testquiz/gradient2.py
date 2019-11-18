from testquiz.SimpleGraphics import *
from tkinter import *


class QuizApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        self.switch_frame(HomeScreen)
        self.geometry("600x500")
        self.getGradient()

        # check size of screen
        # height = self.winfo_screenheight()
        # width = self.winfo_screenwidth()
        # pixels = str(width) + 'x' + str(height)
        # self.geometry(pixels)

    def getGradient(self):
        # draw gradient
        for row in range(0, 800):
            red = row / (getHeight() - 1) * 255
            green = row / (getHeight() - 1) * 192
            blue = row / (getHeight() - 1) * 64

            setColor(red, green, blue)

            # draw line
            line(0, row, getWidth() - 1, row)


    def switch_frame(self, frame_class, *args):

        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()

        if args:
            self._frame = new_frame
            # button4 = Button(self, text=args, fg='black', relief=FLAT, width=16).pack()
            server = args
            self._frame.pack()
        else:
            self._frame = new_frame
            self._frame.pack()


# screen HOME
class HomeScreen(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        label1 = Label(self, text='Home', fg='black', font=('arial', 24, 'bold')).pack(side="top", fill="x", pady=5)


# window MAIN
if __name__ == "__main__":
    app = QuizApp()
    app.title('Play Quiz')
    app.mainloop()

