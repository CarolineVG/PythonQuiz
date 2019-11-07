import sqlite3
import threading
import time
from tkinter import *
from Classes.Database import Database
from Classes.Quiz import Quiz
from Classes.Question import Question
from Classes.Sockets import Server

# class QuizApp
class QuizApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        self.switch_frame(HomeScreen)
        self.geometry("600x500")

        # check size of screen
        # height = self.winfo_screenheight()
        # width = self.winfo_screenwidth()
        # pixels = str(width) + 'x' + str(height)
        # self.geometry(pixels)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


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
            # test Quiz Class

            # create new Quiz
            newQuiz = Quiz(1, 'test')
            #newQuiz.addQuizToDatabase()
            newQuiz.getDataFromDatabase()

            # create new Question
            newQuestion = Question(1, 'question', 2, 'a', 'b', 'c', 'd', 60, 10)
            #newQuestion.addQuestionToDatabase()
            newQuestion.getQuestionFromDatabase()

            # to do: change hardcoded question to input from user

            # test: from database to json format to send to server
            newQuestion.sendQuestionToServer()

            s = Server("", 5000)
            s.host()

            # server.addQuestion(question)

            # question = '{"type":"question", "sender": "Host", "id":"' + question['id'] + '", "question": "' + question[
            #     'question'] + '", "options":' + json.dumps(question['options']) + ',"time":' + json.dumps(
            #     question['time']) + '}'

            # q = questionValue.get()
            # a1 = answer1Value.get()
            # a2 = answer2Value.get()
            # a3 = answer3Value.get()
            # a4 = answer4Value.get()
            # print(f'{q} ? {a1}, {a2}, {a3}, {a4}')
            #
            # # add to db
            # db = Database()
            # # id=1, quizid=1, solution = b (question b is correct)
            # db.insertData(1, q, 'b', a1, a2, a3, a4)
            # db.getData()
            #
            # conn = sqlite3.connect("Quiz.db")
            # with conn:
            #     cursor = conn.cursor()

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


# screen TEST SERVER SCREEN
class TestServerScreen(Frame):
    # constructor
    def __init__(self, master):
        # create quiz
        Frame.__init__(self, master)

        def insertDataInDatabase():
            # test Quiz Class
            # create new Quiz
            newQuiz = Quiz(1, 'test')
            newQuiz.addQuizToDatabase()
            newQuiz.getDataFromDatabase()

            # create new Question
            newQuestion = Question(1, 'question', 2, 'a', 'b', 'c', 'd', 60, 10)
            newQuestion.addQuestionToDatabase()
            newQuestion.getQuestionFromDatabase()

            # to do: change hardcoded question to input from user

            # test: from database to json format to send to server
            newQuestion.sendQuestionToServer()

        btnDatabase = Button(self, text='Insert databases', fg='black', relief=FLAT, width=16, font=('arial', 20, 'bold'), command=insertDataInDatabase).pack()
        btnStartServer = Button(self, text='Start server', fg='black', relief=FLAT, width=16, font=('arial', 20, 'bold'), command=lambda: master.switch_frame(HostQuizScreen)).pack()
        btnStartQuiz = Button(self, text='Return', fg='black', relief=FLAT, width=16, font=('arial', 20, 'bold'), command=lambda: master.switch_frame(HomeScreen)).pack()


# screen HOST QUIZ
class HostQuizScreen(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        def showQuizes():
            # show all quizes from database
            print('show quizes from database')

            q = Quiz()
            quizes = q.getDataFromDatabase()
            print(f'db: {quizes}')

            for item in quizes:
                print(item)
                # temporary hardcoded link to first quiz
                button1 = Button(self, text=item[1], fg='black', relief=FLAT, width=16, font=('arial', 20, 'bold'),
                                 command=lambda: master.switch_frame(HostQuizWaitingScreen)).pack()


        label1 = Label(self, text='Host Quiz', fg='black', font=('arial', 24, 'bold')).pack(side="top", fill="x", pady=5)

        showQuizes()

        button4 = Button(self, text='Return', fg='black', relief=FLAT,
                            width=16, font=('arial', 20, 'bold'), command=lambda: master.switch_frame(HomeScreen)).pack()


# screen WAITING QUIZ (temporary quiz1)
class HostQuizWaitingScreen(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        global server
        server = Server("192.168.1.231",5000)

        global pleaseStop

        def updateInterface():
            print('update interface')
            outputLabel = Label(self, text=str(len(server.clients)), fg='black', font=('arial', 15, 'bold')).pack()
            while True:
                if pleaseStop:
                    print('in please stop')
                    break
                else:
                    time.sleep(5)
                    print(f'threading')
                    outputLabel = Label(self, text=str(len(server.clients)), fg='black',font=('arial', 15, 'bold')).pack()

        def startServer():
            print("start server")
            # test server
            #server = Server("", 5000)
            server.host()

            global pleaseStop
            pleaseStop = False

            # is quiz still open to players?
            # if server.access:
            #     # listen to connections multiple times?
            #     # vragen aan docent?
            #     # - loopen om de zoveel seconden dit updaten
            #     updateInterface()
            # else:
            #     print("let's start the game!")

            # check if label stays up to date with the connected clients


        def stopThread():
            # stop thread:
            print("stop thread")
            global pleaseStop
            pleaseStop = True

        label1 = Label(self, text='Host Quiz', fg='black', font=('arial', 24, 'bold')).pack(side="top", fill="x", pady=5)
        startServer()


        button4 = Button(self, text='Stop thread (start quiz)', fg='black', relief=FLAT,
                         width=16, font=('arial', 20, 'bold'), command=stopThread).pack()


        button4 = Button(self, text='Return', fg='black', relief=FLAT,
                         width=16, font=('arial', 20, 'bold'), command=lambda: master.switch_frame(HomeScreen)).pack()


        x = threading.Thread(target=updateInterface).start()


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
