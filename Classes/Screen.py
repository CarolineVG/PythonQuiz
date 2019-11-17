import sqlite3
import threading
import time
from tkinter import *
from Classes.Database import Database
from Classes.Quiz import Quiz
from Classes.Question import Question
from Classes.Sockets import Server

# global server var
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

        # check size of screen
        # height = self.winfo_screenheight()
        # width = self.winfo_screenwidth()
        # pixels = str(width) + 'x' + str(height)
        # self.geometry(pixels)

    def switch_frame(self, frame_class, *args):

        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()

        if args:
            self._frame = new_frame
            print("Dit zijn onze args: "+str(args))
            #button4 = Button(self, text=args, fg='black', relief=FLAT, width=16).pack()
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

        button1 = Button(self, text='Create quiz', fg='black', relief=FLAT, width=16,
                            font=('arial', 20, 'bold'), command=lambda: master.switch_frame(CreateQuizScreen)).pack()
        button2 = Button(self, text='Host quiz', fg='black', relief=FLAT,
                            width=16, font=('arial', 20, 'bold'), command=lambda: master.switch_frame(HostQuizScreen, 'a')).pack()
        button3 = Button(self, text='Play quiz', fg='black', relief=FLAT,
                            width=16, font=('arial', 20, 'bold'), command=lambda: master.switch_frame(JoinQuizScreen)).pack()


# screen CREATE QUIZ
class CreateQuizScreen(Frame):
    # constructor
    def __init__(self, master):
        # create quiz
        Frame.__init__(self, master)

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
class CreateQuestionScreen(Frame):
    # constructor
    def __init__(self, master):
        # create quiz
        Frame.__init__(self, master)

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

        button1 = Button(self, text='Save and next question', fg='black', relief=FLAT, width=16, font=('arial', 20, 'bold'), command=test).pack()
        button2 = Button(self, text='Finish quiz', fg='black', relief=FLAT, width=16, font=('arial', 20, 'bold'), command=lambda: master.switch_frame(HostQuizScreen)).pack()

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
    def __init__(self, master, *args):
        if args:
            self.args = args
            print("args in hostQuizScreen: " + str(self.args))

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
                # can't pass vars via classes, use global var hostQuiz?
                button1 = Button(self, text=item[1], fg='black', relief=FLAT, width=16, font=('arial', 20, 'bold'),
                                 command=lambda: master.switch_frame(HostQuizWaitingScreen)).pack()


        label1 = Label(self, text='Host Quiz', fg='black', font=('arial', 24, 'bold')).pack(side="top", fill="x", pady=5)

        showQuizes()

        button4 = Button(self, text='Return', fg='black', relief=FLAT, width=16, font=('arial', 20, 'bold'),
                         command=lambda: master.switch_frame(HomeScreen)).pack()


# screen WAITING QUIZ (temporary quiz1)
class HostQuizWaitingScreen(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        # var server
        self.server = Server("", 5000)
        self.stopThread = False

        global server
        server = self.server

        def updateInterface():
            print('update interface')
            amountOfPlayers = len(self.server.clients)
            outputLabel = Label(self, text=str(len(self.server.clients)), fg='black', font=('arial', 15, 'bold')).pack()
            while True:
                if self.stopThread:
                    print('in please stop')
                    self.server.stopHosting()
                    server = self.server
                    # temporary hardcoded
                    # start quiz
                    button4 = Button(self, text='Start Quiz', fg='black', relief=FLAT, width=16, font=('arial', 20, 'bold'),
                                     command=lambda: master.switch_frame(HostQuizStartScreen)).pack()
                    break
                else:
                    time.sleep(2)
                    print(f'threading')
                    if amountOfPlayers == len(self.server.clients):
                        # don't update label
                        print('dont update')
                    else:
                        outputLabel = Label(self, text=str(len(self.server.clients)), fg='black',font=('arial', 15, 'bold'))
                        amountOfPlayers = len(self.server.clients)

        def startServer():
            print("start server")
            self.server.host()

        def stopThread():
            # stop thread:
            print("stop thread")
            self.stopThread = True


        label1 = Label(self, text='Host Quiz', fg='black', font=('arial', 24, 'bold')).pack(side="top", fill="x", pady=5)

        startServer()

        button4 = Button(self, text='Stop thread', fg='black', relief=FLAT,
                         width=16, font=('arial', 20, 'bold'), command=stopThread).pack()

        button4 = Button(self, text='Return', fg='black', relief=FLAT,
                         width=16, font=('arial', 20, 'bold'), command=lambda: master.switch_frame(HomeScreen)).pack()

        x = threading.Thread(target=updateInterface).start()


# screen JOIN QUIZ
class HostQuizStartScreen(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
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
            self.server.waitAndSendScores()

            # self.server.setQuestionList([  # list of (for now hard-coded) questions that the clients will answer
            #     {
            #         'id': '0001',
            #         'question': 'What is the first letter of the alphabet?',
            #         'options': {
            #             'A': 'A',
            #             'B': 'B',
            #             'C': 'C',
            #             'D': 'D'
            #         },
            #         'solution': 'A'
            #     },
            #     {
            #         'id': '0002',
            #         'question': 'What colour is the sky?',
            #         'options': {
            #             'A': 'Green',
            #             'B': 'Red',
            #             'C': 'Blue',
            #             'D': 'brown'
            #         },
            #         'solution': 'C',
            #         'time': 30
            #     },
            #     {
            #         'id': '0003',
            #         'question': 'Who is the best python programmer?',
            #         'options': {
            #             'A': 'Roel',
            #             'B': 'Caroline',
            #             'C': 'Santa Claus'
            #         },
            #         'solution': 'B'
            #     },
            #     {
            #         'id': '0004',
            #         'question': 'What is the airspeed velocity of an unladen swallow?',
            #         'options': {
            #             'A': 'I don\'t know that.',
            #             'B': 'Blue!',
            #             'C': 'That depends. Is it an African swallow or a European one?'
            #         },
            #         'solution': 'C',
            #         'time': 30
            #     },
            #     {
            #         'id': '0005',
            #         'question': 'Was this a fun quiz?',
            #         'options': {
            #             'A': 'Yes!',
            #             'B': 'No.'
            #         },
            #         'solution': 'B'
            #     }
            # ])

            # self.server.handleNextQuestion()
            # self.server.waitAndSendScores()

            # print(f'access: {self.server.access}')
            # print(f'ready: {self.server.ready}')
            # print(f'clients: {self.server.clients}')
            # print(f'questinslist: {self.server.questionList}')
            # print(f'current question: {self.server.currentQuestion}')
            # print(f'scores: {self.server.scores}')
            # print(f'answers: {self.server.answers}')


        # PROBLEM: new screen only shows AFTER players answer first question
        label1 = Label(self, text='Players are answering...', fg='black', font=('arial', 24, 'bold')).pack(side="top", fill="x", pady=5)

        sendFirstQuestion()


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
