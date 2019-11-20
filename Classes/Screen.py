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
            print("args === "+str(args))
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
        print(f'arguments: {self.args}')

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
        self.master = master

        if args:
            self.getArguments(*args)

        label1 = Label(self, text='Host Quiz', fg='black', bg='#FE715B', font=('arial', 24, 'bold')).pack(side="top", fill="x", pady=5)

        label2 = Label(self, text='Enter your ip:', fg='black', bg='#FE715B', font=('arial', 24, 'bold')).pack(side="top", fill="x", pady=5)

        self.ip = ""
        
        input = Entry(self, textvar=self.ip).pack()
        
        label3 = Label(self, text='Choose which quiz to host:', fg='black', bg='#FE715B', font=('arial', 24, 'bold')).pack(side="top", fill="x", pady=5)

        self.showQuizes()

        button4 = Button(self, text='Return', fg='black', relief=FLAT, width=16, font=('arial', 20, 'bold'), command=lambda: master.switch_frame(HomeScreen)).pack()


    def showQuizes(self):
        # show all quizes from database
        print('show quizes from database')

        q = Quiz()
        quizes = q.getDataFromDatabase()
        print(f'db: {quizes}')

        for item in quizes:
            print("Item in quizes = "+str(item))
            quizId = item[0]
            button1 = Button(self, text=item[1], fg='black', relief=FLAT, width=16, font=('arial', 20, 'bold'), command=lambda quizId=quizId: self.next(quizId)).pack()

    def next(self, quizId):
        ip = str(self.ip)
        server = Server(ip, 5000)

        print("this should be our quiz id -> "+str(quizId))
        q = Question()
        questions = q.createQuizWithQuestions(quizId)
        print("this should be a question list -> "+str(questions))
        
        server.setQuestionList(questions)
        self.master.switch_frame(HostQuizWaitingScreen, server)
        
'''
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
'''

# screen WAITING QUIZ (temporary quiz1)
class HostQuizWaitingScreen(BaseScreen):
    # master = self from QuizApp
    def __init__(self, master, *args):

        # extend from BaseScreen
        BaseScreen.__init__(self, master)
        self.master = master

        if args:
            self.getArguments(*args)

        # var server
        self.server = self.args[0]
        self.start = False

        label1 = Label(self, text='Host Quiz', fg='black', font=('arial', 24, 'bold')).pack(side="top", fill="x", pady=5)
        self.startServer()

        self.waitingLabel = Label(self, text='Waiting for players...', fg='black', font=('arial', 12, 'bold'))
        self.waitingLabel.pack(side="top", fill="x", pady=5)
        
        self.playersLabel = Label(self, text=f"{str(len(self.server.clients))} players are connected", fg='black',font=('arial', 15, 'bold'))
        self.playersLabel.pack()

        self.continueButton = Button(self, text='Enough players', fg='black', relief=FLAT, width=16, font=('arial', 20, 'bold'), command=lambda: self.stopThread())
        self.continueButton.pack()
        
        button2 = Button(self, text='Return', fg='black', relief=FLAT, width=16, font=('arial', 20, 'bold'), command=lambda: master.switch_frame(HomeScreen)).pack()

        #IMPORTANT: when we return, we probably have to shut down the server instance so it can be started again on the previous screen
        #I don't know how to do this
        #halp

        x = threading.Thread(target=self.updateInterface).start()

    def updateInterface(self):
        amountOfPlayers = len(self.server.clients)
        
        while True:
            if self.start:
                self.server.stopHosting()
                server = self.server
                self.continueButton.config(text='Start Quiz', command=lambda: self.master.switch_frame(HostQuizStartScreen, self.server, 0))
                self.waitingLabel.config(text = "Ready to begin")
                break
            else:
                self.playersLabel.config(text = f"{str(len(self.server.clients))} players are connected")
    def startServer(self):
        print("start server")
        self.server.host()

    def stopThread(self):
        # stop thread:
        print("stop thread")
        self.start = True


class HostQuizStartScreen(BaseScreen):
    # master = self from QuizApp
    def __init__(self, master, *args):

        # extend from BaseScreen
        BaseScreen.__init__(self, master)

        if args:
            self.getArguments(*args)

        self.server = self.args[0]
        
        #at what question are we? If no position is specified, this is the first question.
        if len(self.args) > 1 and self.args[1] == 0:
            print("hier")
            position = self.args[1]
            print(position)
            button = Button(self, text='Send the first question!', fg='black', relief=FLAT, width=16, font=('arial', 20, 'bold'),command=lambda: master.switch_frame(HostQuizQuestionScreen, self.server, position))
            button.pack()
        else:
            print("daar")
            position = self.args[1]
            button = Button(self, text='Send the next question!', fg='black', relief=FLAT, width=16, font=('arial', 20, 'bold'), command=lambda: master.switch_frame(HostQuizQuestionScreen, self.server, position)).pack()

        

    '''
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
    '''

class HostQuizQuestionScreen(BaseScreen):
    # master = self from QuizApp
    def __init__(self, master, *args):

        print("in HostQuizQuestionScreen constructor")

        # extend from BaseScreen
        BaseScreen.__init__(self, master)

        if args:
            self.getArguments(*args)

        self.server = self.args[0]
        
        self.position = self.args[1]

        self.server.handleNextQuestion()
        label1 = Label(self, text='Players are answering...', fg='black', font=('arial', 24, 'bold')).pack(side="top", fill="x", pady=5)

        self.server.waitAndSendScores()
        # show scoreboard

# screen JOIN QUIZ
class JoinQuizScreen(BaseScreen):
    # master = self from QuizApp
    def __init__(self, master, *args):

        # extend from BaseScreen
        BaseScreen.__init__(self, master)

        if args:
            self.getArguments(*args)

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
