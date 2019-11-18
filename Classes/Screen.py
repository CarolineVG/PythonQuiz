import sqlite3
import threading
import time
from tkinter import *
from Classes.Database import Database
from Classes.Quiz import Quiz
from Classes.Question import Question
from Classes.Sockets import Server


from PIL import Image, ImageDraw, ImageTk

# global server var AANPASSEN GEEN GLOBAL VARS GEBRUIKEN!!
server = ''
hostQuiz = 0
createQuizId = 0

# class QuizApp
class QuizApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        self.switch_frame(HomeScreen)
        self.geometry("600x500")
        self.configure(bg='#FE715B')

        # check size of screen
        #height = self.winfo_screenheight()
        #width = self.winfo_screenwidth()
        #pixels = str(width - 10) + 'x' + str(height)
        #self.geometry(pixels)

    # switch screens
    def switch_frame(self, frame_class, *args):
        # frame_class = any class that has been given as a parameter
        # assign self from QuizApp to frame_class
        if args:
            new_frame = frame_class(self, args)
        else:
            new_frame = frame_class(self)

        # destroy current frame
        if self._frame is not None:
            self._frame.destroy()

        # assign new frame and show it
        self._frame = new_frame
        self._frame.pack()


# class BASESCREEN extends from frame, other screen classes will extend from basescreen
class BaseScreen(Frame):
    # constructor
    def __init__(self, master):
        Frame.__init__(self, master)

        # layout vars
        self.font='arial'
        #self.buttonSize
        # to do: colors, sizes



        #button1 = Button(self, text='Create quiz', fg='black', bg='white', relief=FLAT, borderwidth=2, width=16,
        # font=('arial', 20, 'bold'), command=lambda: master.switch_frame(CreateQuizScreen)).
        # pack(side="top", fill="x", pady=20)

    # get args
    def getArguments(self, args):
        self.args = args

    def createButton(self, text, type, method):
        if type == None:
            type = "default"

        # type buttons
        # default:
        # return:
        # confirm:

        # methods:
        # function or switch screen

        # type (basic,...), method: , colors:
        basicButton = Button(self, text=text, fg='black', bg='white', relief=FLAT, borderwidth=2,
                                  width=16, font=('arial', 20, 'bold'))

        return basicButton

    # create label function


# TEST screen
class TestScreen(BaseScreen):
    # master = self from QuizApp
    def __init__(self, master, *args):

        # extend from BaseScreen
        BaseScreen.__init__(self, master)

        if args:
            self.getArguments(*args)
            print(f'arguments: {self.args}')


        # bg color
        self.configure(bg='#FE715B')

        self.createButton('a', 'b', 'c').pack()


        label1 = Label(self, text=self.args, fg='#850001', bg='#FE715B', font=('arial', 24, 'bold')).pack(side="top", fill="x", pady=30)


# home
class HomeScreen(BaseScreen):
    # master = self from QuizApp
    def __init__(self, master, *args):

        # extend from BaseScreen
        BaseScreen.__init__(self, master)

        if args:
            self.getArguments(*args)
            print(f'arguments: {self.args}')


        # bg color
        self.configure(bg='#FE715B')

        label1 = Label(self, text='Home', fg='#850001', bg='#FE715B', font=('arial', 24, 'bold')).pack(side="top", fill="x", pady=30)

        button1 = Button(self, text='Create quiz', fg='black', bg='white', relief=FLAT, borderwidth=2, width=16,
                            font=('arial', 20, 'bold'), command=lambda: master.switch_frame(CreateQuizScreen)).pack(side="top", fill="x", pady=20)
        button2 = Button(self, text='Host quiz', fg='black', bg='white', relief=FLAT,
                            width=16, font=('arial', 20, 'bold'), command=lambda: master.switch_frame(HostQuizScreen, 'a')).pack(side="top", fill="x", pady=20)
        button3 = Button(self, text='Play quiz', fg='black', bg='white', relief=FLAT,
                            width=16, font=('arial', 20, 'bold'), command=lambda: master.switch_frame(JoinQuizScreen)).pack(side="top", fill="x", pady=20)



        button4 = Button(self, text='Test', fg='black', bg='white', relief=FLAT,
                                 width=16, font=('arial', 20, 'bold'),
                                 command=lambda: master.switch_frame(TestScreen, 1, 2)).pack(side="top", fill="x", pady=20)


# screen CREATE QUIZ
class CreateQuizScreen(BaseScreen):
    # master = self from QuizApp
    def __init__(self, master, *args):

        # extend from BaseScreen
        BaseScreen.__init__(self, master)

        if args:
            self.getArguments(*args)
            print(f'arguments: {self.args}')


        def saveQuiz():
            q = quizValue.get()
            print(f'new quiz: {q}')

            # create new Quiz
            newQuiz = Quiz()
            newQuiz.setQuizName(q)
            newQuiz.addQuizToDatabase()

            # get id from new quiz
            result = newQuiz.getIdFromQuizName(q)
            global createQuizId
            createQuizId = result[0]
            print(createQuizId)

            # change layout
            button2 = Button(self, text='Add questions', fg='black', relief=FLAT, width=16, font=('arial', 20, 'bold'),
                             command=lambda: master.switch_frame(CreateQuestionScreen)).pack()

        quizValue = StringVar()

        pinLabel = Label(self, text='Quiz', fg='black', font=('arial', 24, 'bold')).pack()

        questionLabel = Label(self, text='Quiz Name*', fg='black', font=('arial', 16, 'bold')).pack()

        questionInput = Entry(self, textvar=quizValue).pack()

        button1 = Button(self, text='Save', fg='black', relief=FLAT, width=16, font=('arial', 20, 'bold'), command=saveQuiz).pack()

        button3 = Button(self, text='Return', fg='black', relief=FLAT, width=16, font=('arial', 20, 'bold'), command=lambda: master.switch_frame(HomeScreen)).pack()


# screen CREATE QUESTION QUIZ
class CreateQuestionScreen(BaseScreen):
    # master = self from QuizApp
    def __init__(self, master, *args):

        # extend from BaseScreen
        BaseScreen.__init__(self, master)

        if args:
            self.getArguments(*args)
            print(f'arguments: {self.args}')

        def test():
            # create new Quiz
            print(f'Quiz Id: {createQuizId}')

            q = questionValue.get()
            a1 = answer1Value.get()
            a2 = answer2Value.get()
            a3 = answer3Value.get()
            a4 = answer4Value.get()
            s = solutionValue.get()

            # create new Question: temp: 2 = solution
            newQuestion = Question()
            newQuestion.addQuestion(createQuizId, q, s, a1, a2, a3, a4, 60, 10)
            newQuestion.addQuestionToDatabase()
            newQuestion.getQuestionFromDatabase()

            # to do: change hardcoded question to input from user

            # test: from database to json format to send to server
            # newQuestion.sendQuestionToServer()
            #
            # s = Server("", 5000)
            # s.host()

            # server.addQuestion(question)

            # question = '{"type":"question", "sender": "Host", "id":"' + question['id'] + '", "question": "' + question[
            #     'question'] + '", "options":' + json.dumps(question['options']) + ',"time":' + json.dumps(
            #     question['time']) + '}'

            # empty everything for new question
            # TO DO...

        questionValue = StringVar()
        answer1Value = StringVar()
        answer2Value = StringVar()
        answer3Value = StringVar()
        answer4Value = StringVar()
        solutionValue = StringVar()

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

        solutionLabel = Label(self, text='Correct answer', fg='black', font=('arial', 16, 'bold')).pack()
        r1 = Radiobutton(self, text='1', variable=solutionValue, value='option1').pack()
        r2 = Radiobutton(self, text='2', variable=solutionValue, value='option2').pack()
        r3 = Radiobutton(self, text='3', variable=solutionValue, value='option3').pack()
        r4 = Radiobutton(self, text='4', variable=solutionValue, value='option4').pack()

        button1 = Button(self, text='Save and next question', fg='black', relief=FLAT, width=16,
                         font=('arial', 20, 'bold'), command=test).pack()
        button2 = Button(self, text='Finish quiz', fg='black', relief=FLAT, width=16, font=('arial', 20, 'bold'),
                         command=lambda: master.switch_frame(HostQuizScreen)).pack()

        button3 = Button(self, text='Return', fg='black', relief=FLAT, width=16, font=('arial', 20, 'bold'),
                         command=lambda: master.switch_frame(HomeScreen)).pack()


# screen HOST QUIZ
class HostQuizScreen(BaseScreen):
    # master = self from QuizApp
    def __init__(self, master, *args):

        # extend from BaseScreen
        BaseScreen.__init__(self, master)

        if args:
            self.getArguments(*args)
            print(f'arguments: {self.args}')

        def showQuizes():
            # show all quizes from database
            print('show quizes from database')

            q = Quiz()
            quizes = q.getDataFromDatabase()
            print(f'db: {quizes}')

            for item in quizes:
                print(item)
                # temporary hardcoded link to first quiz
                # can't pass vars via classes, use global var hostQuiz?
                button1 = Button(self, text=item[1], fg='black', relief=FLAT, width=16, font=('arial', 20, 'bold'),
                                 command=lambda: master.switch_frame(HostQuizWaitingScreen)).pack()


        label1 = Label(self, text='Host Quiz', fg='black', font=('arial', 24, 'bold')).pack(side="top", fill="x", pady=5)

        showQuizes()

        button4 = Button(self, text='Return', fg='black', relief=FLAT, width=16, font=('arial', 20, 'bold'),
                         command=lambda: master.switch_frame(HomeScreen)).pack()


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


# screen WAITING QUIZ (temporary quiz1)
class HostQuizWaitingScreen(BaseScreen):
    # master = self from QuizApp
    def __init__(self, master, *args):

        # extend from BaseScreen
        BaseScreen.__init__(self, master)

        if args:
            self.getArguments(*args)
            print(f'arguments: {self.args}')

        # var server
        self.server = Server("", 5000)
        self.stopThread = False

        global server
        server = self.server

        def updateInterface():
            print('update interface')
            amountOfPlayers = len(self.server.clients)
            outputLabel = Label(self, text=str(len(self.server.clients)), fg='black',
                                    font=('arial', 15, 'bold'))
            outputLabel.pack()
            print('eerste test: ' + str(outputLabel))

            while True:
                if self.stopThread:
                    print('in please stop')
                    self.server.stopHosting()
                    server = self.server
                    # temporary hardcoded
                    # start quiz
                    button4 = Button(self, text='Start Quiz', fg='black', relief=FLAT, width=16,
                                         font=('arial', 20, 'bold'),
                                         command=lambda: master.switch_frame(HostQuizStartScreen)).pack()
                    break
                else:
                    time.sleep(2)
                    outputLabel.config(text = str(len(self.server.clients)))

        def startServer():
            print("start server")
            self.server.host()

        def stopThread():
            # stop thread:
            print("stop thread")
            self.stopThread = True

        label1 = Label(self, text='Host Quiz', fg='black', font=('arial', 24, 'bold')).pack(side="top", fill="x",
                                                                                                pady=5)

        startServer()

        button4 = Button(self, text='Stop thread', fg='black', relief=FLAT,
                             width=16, font=('arial', 20, 'bold'), command=stopThread).pack()

        button4 = Button(self, text='Return', fg='black', relief=FLAT,
                             width=16, font=('arial', 20, 'bold'),
                             command=lambda: master.switch_frame(HomeScreen)).pack()

        x = threading.Thread(target=updateInterface).start()


class HostQuizStartScreen(BaseScreen):
    # master = self from QuizApp
    def __init__(self, master, *args):

        # extend from BaseScreen
        BaseScreen.__init__(self, master)

        if args:
            self.getArguments(*args)
            print(f'arguments: {self.args}')

        # get server object from global server
        self.server = server
        print(f'server start screen: {self.server}')

        # server object from hostquiz waiting screen

        def sendFirstQuestion():
            # import from db with correct quizId
            quizId = 1
            newQuestion = Question()
            quiz = newQuestion.createQuizWithQuestions(quizId)

            self.server.setQuestionList(quiz)

            self.server.handleNextQuestion()

            # waiting screen that informs player that all questions are being answered

            self.server.waitAndSendScores()


            # show scoreboard to players
            # to do new screen:





        # PROBLEM: new screen only shows AFTER players answer first question
        label1 = Label(self, text='Players are answering...', fg='black', font=('arial', 24, 'bold')).pack(
                side="top", fill="x", pady=5)

        sendFirstQuestion()


# screen JOIN QUIZ
class JoinQuizScreen(BaseScreen):
    # master = self from QuizApp
    def __init__(self, master, *args):

        # extend from BaseScreen
        BaseScreen.__init__(self, master)

        if args:
            self.getArguments(*args)
            print(f'arguments: {self.args}')

        # input vars
        pinValue = StringVar()
        usernameValue = StringVar()

        label1 = Label(self, text='Join Quiz', fg='black', font=('arial', 24, 'bold')).pack(side="top", fill="x",
                                                                                                pady=5)

        pinLabel = Label(self, text='Enter pin', fg='black', font=('arial', 16, 'bold')).pack()
        pinInput = Entry(self, textvar=pinValue).pack()

        usernameLabel = Label(self, text='Enter username', fg='black', font=('arial', 16, 'bold')).pack()
        usernameInput = Entry(self, textvar=usernameValue).pack()

        button1 = Button(self, text='Participate', fg='black', relief=FLAT, width=16,
                             font=('arial', 20, 'bold')).pack()
        button2 = Button(self, text='Return', fg='black', relief=FLAT,
                             width=16, font=('arial', 20, 'bold'),
                             command=lambda: master.switch_frame(HomeScreen)).pack()
