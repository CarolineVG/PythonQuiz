from tkinter import *

# quiz app
class QuizApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        self.switch_frame(HomeScreen)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

# screen HOME
class HomeScreen(Frame):
    def __init__(self, master):
        # home page

        Frame.__init__(self, master)

        label1 = Label(self, text='Home', fg='black', font=('arial', 24, 'bold')).pack(side="top", fill="x", pady=5)

        button1 = Button(self, text='Create quiz', fg='black', relief=FLAT, width=16,
                            font=('arial', 20, 'bold'), command=lambda: master.switch_frame(CreateQuizScreen)).pack()
        button2 = Button(self, text='Host quiz', fg='black', relief=FLAT,
                            width=16, font=('arial', 20, 'bold')).pack()
        button3 = Button(self, text='Play quiz', fg='black', relief=FLAT,
                            width=16, font=('arial', 20, 'bold')).pack()

# screen CREATE QUIZ
class CreateQuizScreen(Frame):
    # constructor
    def __init__(self, master):
        # create quiz
        Frame.__init__(self, master)

        def test():
            q = questionValue.get()
            a1 = answer1Value.get()
            a2 = answer2Value.get()
            a3 = answer3Value.get()
            print(f'{q} ? {a1}, {a2}, {a3}')

        questionValue = StringVar()
        answer1Value = StringVar()
        answer2Value = StringVar()
        answer3Value = StringVar()
        answer4Value = StringVar()

        pinLabel = Label(self, text='Quiz', fg='black', font=('arial', 24, 'bold')).pack()

        questionLabel = Label(self, text='Question', fg='black', font=('arial', 16, 'bold')).pack()
        questionInput = Entry(self, textvar=questionValue).pack()

        answer1Label = Label(self, text='Answer 1 (correct answer)', fg='black', font=('arial', 16, 'bold')).pack()
        answer1Input = Entry(self, textvar=answer1Value).pack()

        answer2Label = Label(self, text='Answer 2', fg='black', font=('arial', 16, 'bold')).pack()
        answer2Input = Entry(self, textvar=answer2Value).pack()

        answer3Label = Label(self, text='Answer 3 (optional)', fg='black', font=('arial', 16, 'bold')).pack()
        answer3Input = Entry(self, textvar=answer3Value).pack()

        answer4Label = Label(self, text='Answer 4 (optional)', fg='black', font=('arial', 16, 'bold')).pack()
        answer4Input = Entry(self, textvar=answer4Value).pack()

        button1 = Button(self, text='Next question', fg='black', relief=FLAT, width=16, font=('arial', 20, 'bold'), command=test).pack()
        button2 = Button(self, text='Finish quiz', fg='black', relief=FLAT, width=16, font=('arial', 20, 'bold')).pack()


# window MAIN
if __name__ == "__main__":
    app = QuizApp()
    app.geometry('375x667')
    app.title('Play Quiz')
    app.mainloop()
