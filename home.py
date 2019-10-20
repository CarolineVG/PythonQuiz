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
class Database:

    def __init__(self):
        # quizes
        self.conn = sqlite3.connect("Quiz.db")
        self.cursor = self.conn.cursor()
        self.conn.execute('CREATE TABLE IF NOT EXISTS Quizes(Id INTEGER NOT NULL PRIMARY KEY, quizName TEXT, Description TEXT)')
        # questions
        self.conn.execute('CREATE TABLE IF NOT EXISTS Questions(Id INTEGER NOT NULL PRIMARY KEY, QuizId NUMBER, Question TEXT, Solution NUMBER, Answer1 TEXT, Answer2 TEXT, Answer3 TEXT, Answer4 TEXT)')
        self.conn.commit()

    def closeConnection(self):
        self.conn.close()

    # get data
    def getData(self):
        self.cursor.execute('SELECT * FROM Questions')
        records = self.cursor.fetchall()
        print(f'data from db: {records}')
        self.conn.commit()

    # insert data
    def insertData(self, quizId, question, solution, answer1, answer2, answer3, answer4):
        self.conn.execute('INSERT INTO Questions(QuizId, Question, Solution, Answer1, Answer2, Answer3, Answer4) VALUES(?,?,?,?,?,?,?)', (quizId, question, solution, answer1, answer2, answer3, answer4))
        self.conn.commit()

        # this does work!
        self.cursor.execute('SELECT * FROM Questions')
        records = self.cursor.fetchall()
        print(f'after db - {records}')


# class Quiz
class Question:
    questionNumber = 0

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.email = first + '.' + last + '@email.com'
        self.pay = pay

    def fullname(self):
        return '{} {}'.format(self.first, self.last)

    def apply_raise(self):
            self.pay = int(self.pay * self.raise_amt)


# screen HOME
class HomeScreen(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        label1 = Label(self, text='Home', fg='black', font=('arial', 24, 'bold')).pack(side="top", fill="x", pady=5)

        button1 = Button(self, text='Create quiz', fg='black', relief=FLAT, width=16,
                            font=('arial', 20, 'bold'), command=lambda: master.switch_frame(CreateQuizScreen)).pack()
        button2 = Button(self, text='Host quiz', fg='black', relief=FLAT,
                            width=16, font=('arial', 20, 'bold'), command=lambda: master.switch_frame(HostQuizScreen)).pack()
        button3 = Button(self, text='Play quiz', fg='black', relief=FLAT,
                            width=16, font=('arial', 20, 'bold'), command=lambda: master.switch_frame(JoinQuizScreen)).pack()


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
            # id=1, quizid=1, solution = b (question b is correct)
            db.insertData(1, q, 'b', a1, a2, a3, a4)
            db.getData()

            conn = sqlite3.connect("Quiz.db")
            with conn:
                cursor = conn.cursor()

        questionValue = StringVar()
        answer1Value = StringVar()
        answer2Value = StringVar()
        answer3Value = StringVar()
        answer4Value = StringVar()

        pinLabel = Label(self, text='Quiz', fg='black', font=('arial', 24, 'bold')).pack()

        questionLabel = Label(self, text='Question*', fg='black', font=('arial', 16, 'bold')).pack()
        questionInput = Entry(self, textvar=questionValue).pack()

        answer1Label = Label(self, text='Answer 1*', fg='black', font=('arial', 16, 'bold')).pack()
        answer1Input = Entry(self, textvar=answer1Value).pack()

        answer2Label = Label(self, text='Answer 2*', fg='black', font=('arial', 16, 'bold')).pack()
        answer2Input = Entry(self, textvar=answer2Value).pack()

        answer3Label = Label(self, text='Answer 3', fg='black', font=('arial', 16, 'bold')).pack()
        answer3Input = Entry(self, textvar=answer3Value).pack()

        answer4Label = Label(self, text='Answer 4', fg='black', font=('arial', 16, 'bold')).pack()
        answer4Input = Entry(self, textvar=answer4Value).pack()

        button1 = Button(self, text='Next question', fg='black', relief=FLAT, width=16, font=('arial', 20, 'bold'), command=test).pack()
        button2 = Button(self, text='Finish quiz', fg='black', relief=FLAT, width=16, font=('arial', 20, 'bold')).pack()

        button3 = Button(self, text='Return', fg='black', relief=FLAT, width=16, font=('arial', 20, 'bold'), command=lambda: master.switch_frame(HomeScreen)).pack()


# screen HOST QUIZ
class HostQuizScreen(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        label1 = Label(self, text='Host Quiz', fg='black', font=('arial', 24, 'bold')).pack(side="top", fill="x", pady=5)

        button1 = Button(self, text='Quiz 1', fg='black', relief=FLAT, width=16,
                            font=('arial', 20, 'bold')).pack()
        button2 = Button(self, text='Quiz 2', fg='black', relief=FLAT,
                            width=16, font=('arial', 20, 'bold')).pack()
        button3 = Button(self, text='Quiz 3', fg='black', relief=FLAT,
                            width=16, font=('arial', 20, 'bold')).pack()
        button4 = Button(self, text='Return', fg='black', relief=FLAT,
                            width=16, font=('arial', 20, 'bold'), command=lambda: master.switch_frame(HomeScreen)).pack()


# screen JOIN QUIZ
class JoinQuizScreen(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        # input vars
        pinValue = StringVar()
        usernameValue = StringVar()

        label1 = Label(self, text='Join Quiz', fg='black', font=('arial', 24, 'bold')).pack(side="top", fill="x", pady=5)

        pinLabel = Label(self, text='Enter pin', fg='black', font=('arial', 16, 'bold')).pack()
        pinInput = Entry(self, textvar=pinValue).pack()

        usernameLabel = Label(self, text='Enter username', fg='black', font=('arial', 16, 'bold')).pack()
        usernameInput = Entry(self, textvar=usernameValue).pack()

        button1 = Button(self, text='Participate', fg='black', relief=FLAT, width=16, font=('arial', 20, 'bold')).pack()
        button2 = Button(self, text='Return', fg='black', relief=FLAT,
                            width=16, font=('arial', 20, 'bold'), command=lambda: master.switch_frame(HomeScreen)).pack()


# window MAIN
if __name__ == "__main__":
    app = QuizApp()
    app.geometry('375x667')
    app.title('Play Quiz')
    app.mainloop()
