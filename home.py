import sqlite3
from tkinter import *


# class QuizApp
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

# class Database
# NOG DB ID TOEVOEGEN AS PRIMARY KEY
class Database():

    def __init__(self):
        self.conn = sqlite3.connect("Quiz.db")
        self.cursor = self.conn.cursor()
        self.conn.execute('CREATE TABLE IF NOT EXISTS Questions(Question TEXT, CorrectAnswer TEXT, WrongAnswerOne TEXT, WrongAnswerTwo TEXT, WrongAnswerThree TEXT)')
        self.conn.commit()

    def closeConnection(self):
        self.conn.close()

    # get data: DOESNT WORK
    def getData(self):
        # self.conn = sqlite3.connect("Quiz.db")
        # with self.conn:
        #     self.cursor = self.conn.cursor()
        #
        self.conn.execute('SELECT * FROM Questions')
        self.conn.commit()
        records = self.cursor.fetchall()
        print(f'data from db: {records}')
        return records

    # insert data
    def insertData(self, question, correctAnswer, wrongAnswerOne, wrongAnswerTwo, wrongAnswerThree):
        self.conn.execute('INSERT INTO Questions(Question, CorrectAnswer, WrongAnswerOne, WrongAnswerTwo, WrongAnswerThree) VALUES(?,?,?,?,?)', (question, correctAnswer, wrongAnswerOne, wrongAnswerTwo, wrongAnswerThree))
        self.conn.commit()

        # this does work!
        self.cursor.execute('SELECT * FROM Questions')
        records = self.cursor.fetchall()
        print(f'after db - {records}')


# class Quiz
# to do ...

# class Question
# to do ...

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
            a4 = answer4Value.get()
            print(f'{q} ? {a1}, {a2}, {a3}, {a4}')

            # add to db
            db = Database()
            db.insertData(q, a1, a2, a3, a4)
            #db.getData()

            conn = sqlite3.connect("Quiz.db")
            with conn:
                cursor = conn.cursor()

            conn.execute('SELECT * FROM Questions')
            conn.commit()
            records = cursor.fetchall()
            print(f'data from db: {records}')



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
