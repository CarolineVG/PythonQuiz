import threading
import time
from tkinter import *
from Classes.Quiz import Quiz
from Classes.Question import Question
from Classes.Sockets import Server
from Classes.Sockets import Client


# global server var AANPASSEN GEEN GLOBAL VARS GEBRUIKEN!!
createQuizId = 0

# class QuizApp
class QuizApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        self.switch_frame(HomeScreen)
        self.geometry("600x800")
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

        self.backgroundColor = "#FE715B"

        # -- LABEL --
        self.labelForeColor = "#850001"
        self.labelBackColor = self.backgroundColor
        self.fontFamily = 'arial'
        self.LabelTitleFontSize = 30
        self.labelFontSize = 18
        self.labelFontType = ''

        # -- BUTTON --
        self.buttonForeColor = "#850001"
        self.buttonBackColor = "#FFF"
        self.buttonActiveForeColor = "#850001"
        self.buttonActiveBackColor = "#FFFFF0"
        self.buttonWidth = 18
        self.buttonFontFamily = self.fontFamily
        self.buttonFontSize = 18
        self.buttonFontType = "bold"

        # -- ENTRY --
        self.entryForeColor = "#850001"
        self.entryBackColor = "#FFF"
        self.entryWidth = 18
        self.entryFontFamily = self.fontFamily
        self.entryFontSize = 18
        self.entryFontType = ""

    # get args
    def getArguments(self, args):
        self.args = args
        print(f'arguments: {self.args}')

    def setBackgroundColor(self):
        return self.backgroundColor

    def createButton(self, text, type, method):
        if type == None:
            type = "default"

        # methods:
        # function or switch screen
        newMethod = method

        # type (basic,...), method: , colors:

        # CONFIRM button: bg green
        if type == "confirm":
            newButtonForeColor = "#FFF"
            newButtonBackColor = "green"
            newButtonActiveForeColor = "#FFF"
            newButtonActiveBackColor = "#7BC17E"

            button = Button(self, text=text, fg=newButtonForeColor, bg=newButtonBackColor,
                          activeforeground=newButtonActiveForeColor, activebackground=newButtonActiveBackColor,
                          relief=FLAT, width=self.buttonWidth, font=(self.buttonFontFamily, self.buttonFontSize, self.buttonFontType), command=method)


        # RETURN button bg red
        elif type == "return":
            newButtonForeColor = "#FFF"
            newButtonBackColor = "#92050C"
            newButtonActiveForeColor = "#FFF"
            newButtonActiveBackColor = "#92050C"

            button = Button(self, text=text, fg=newButtonForeColor, bg=newButtonBackColor,
                            activeforeground=newButtonActiveForeColor, activebackground=newButtonActiveBackColor,
                            relief=FLAT, width=self.buttonWidth,
                            font=(self.buttonFontFamily, self.buttonFontSize, self.buttonFontType), command=method)

        # DEFAULT button
        elif type == "default":
            # default buttons, no vars to change
            button = Button(self, text=text, fg=self.buttonForeColor, bg=self.buttonBackColor,
                          activeforeground=self.buttonActiveForeColor, activebackground=self.buttonActiveBackColor,
                          relief=FLAT,
                          width=self.buttonWidth,
                          font=(self.buttonFontFamily, self.buttonFontSize, self.buttonFontType), command=method)

        return button

    def createLabel(self, text, type):

        if type == None:
            type = "default"
        # TITLE
        if type == "title":
            newLabelFontSize = 30
            newLabelFontType = 'bold'

            label = Label(self, text=text, fg=self.labelForeColor, bg=self.labelBackColor, font=(self.fontFamily, newLabelFontSize, newLabelFontType))
        # DEFAULT
        elif type == "default":
            label = Label(self, text=text, fg=self.labelForeColor, bg=self.labelBackColor,
                          font=(self.fontFamily, self.labelFontSize, self.labelFontType))

        return label

    def createInput(self, value, type):

        if type == None:
            type = "default"

        # DEFAULT
        if type == "default":
            inputfield = Entry(self, textvar=value, fg = self.entryForeColor, bg = self.entryBackColor, width = self.entryWidth, font = (self.entryFontFamily, self.entryFontSize, self.entryFontType))

        return inputfield


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

        self.createButton('confirm', 'confirm', 'c').pack()
        self.createButton('return', 'return', 'c').pack()
        self.createButton('default', 'default', 'c').pack()


        label1 = Label(self, text=self.args, fg='#850001', bg='#FE715B', font=('arial', 24, 'bold')).pack(side="top", fill="x", pady=30)


# screen HOME
class HomeScreen(BaseScreen):
    # master = self from QuizApp
    def __init__(self, master, *args):

        # extend from BaseScreen
        BaseScreen.__init__(self, master)

        if args:
            self.getArguments(*args)

        # layout
        self.configure(bg=self.setBackgroundColor())

        self.createLabel('Home', 'title').pack(side="top",fill="x",pady=30)

        self.createButton('Create Quiz', 'default', lambda: master.switch_frame(CreateQuizScreen)).pack(side="top", fill="x", pady=20)
        self.createButton('Host Quiz', 'default', lambda: master.switch_frame(HostQuizScreen, 'a')).pack(side="top",fill="x",pady=20)
        self.createButton('Play Quiz', 'default', lambda: master.switch_frame(JoinQuizScreen)).pack(side="top",fill="x",pady=20)
        self.createButton('TEST', 'return', lambda: master.switch_frame(TestScreen, 1, 2)).pack(side="top",fill="x",pady=20)


# screen CREATE QUIZ
class CreateQuizScreen(BaseScreen):
    # master = self from QuizApp
    def __init__(self, master, *args):

        # extend from BaseScreen
        BaseScreen.__init__(self, master)

        if args:
            self.getArguments(*args)

        self.quizValue = StringVar()

        # layout
        self.configure(bg=self.setBackgroundColor())

        self.createLabel('Quiz', 'title').pack(side="top", fill="x", pady=30)

        self.createLabel('Quiz Name*', 'default').pack(side="top", fill="x", pady=30)
        self.createInput(self.quizValue, 'default').pack()

        self.createButton('Save', 'confirm', self.saveQuiz).pack(side="top",fill="x",pady=10)
        self.createButton('Return', 'return', lambda: master.switch_frame(HomeScreen)).pack(side="top",fill="x",pady=10)

    def saveQuiz(self):
        q = self.quizValue.get()

        # create new Quiz
        newQuiz = Quiz()
        newQuiz.setQuizName(q)
        newQuiz.addQuizToDatabase()

        # get id from new quiz
        result = newQuiz.getIdFromQuizName(q)

        createQuizId = result[0]
        print(createQuizId)

        # add questions button
        self.createButton('Add Questions', 'confirm', lambda: self.master.switch_frame(CreateQuestionScreen, createQuizId)).pack(
            side="top", fill="x", pady=10)

        # disable save button and return button (you can't make an empty quiz)
        # to do ...


# screen CREATE QUESTION QUIZ
class CreateQuestionScreen(BaseScreen):
    # master = self from QuizApp
    def __init__(self, master, *args):

        # extend from BaseScreen
        BaseScreen.__init__(self, master)

        if args:
            self.getArguments(*args)

        arg = args[0]
        self.quizId = arg[0]
        print(self.quizId)


        self.questionValue = StringVar()
        self.answer1Value = StringVar()
        self.answer2Value = StringVar()
        self.answer3Value = StringVar()
        self.answer4Value = StringVar()
        self.solutionValue = StringVar()

        # layout
        self.configure(bg=self.setBackgroundColor())

        self.createLabel('Quiz', 'title').pack(side="top", fill="x", pady=30)

        self.createLabel('Question', 'default').pack()
        self.createInput(self.questionValue, 'default').pack()

        self.createLabel('Answer 1', 'default').pack()
        self.createInput(self.answer1Value, 'default').pack()

        self.createLabel('Answer 2', 'default').pack()
        self.createInput(self.answer2Value, 'default').pack()

        self.createLabel('Answer 3', 'default').pack()
        self.createInput(self.answer3Value, 'default').pack()

        self.createLabel('Answer 4', 'default').pack()
        self.createInput(self.answer4Value, 'default').pack()

        # TO DO: LAYOUT
        solutionLabel = Label(self, text='Correct answer', fg='black', font=('arial', 16, 'bold')).pack()
        r1 = Radiobutton(self, text='1', variable=self.solutionValue, value='option1').pack()
        r2 = Radiobutton(self, text='2', variable=self.solutionValue, value='option2').pack()
        r3 = Radiobutton(self, text='3', variable=self.solutionValue, value='option3').pack()
        r4 = Radiobutton(self, text='4', variable=self.solutionValue, value='option4').pack()

        self.createButton('Save and next question', 'confirm', lambda: self.addQuestion()).pack(side="top", fill="x",pady=20)
        self.createButton('Finish Quiz', 'confirm', lambda: master.switch_frame(HostQuizScreen)).pack(side="top", fill="x",pady=20)
        self.createButton('Return', 'return', lambda: master.switch_frame(HomeScreen)).pack(side="top", fill="x",pady=20)

    def addQuestion(self):
        # create new Quiz
        print(f'Quiz Id: {self.quizId}')

        q = self.questionValue.get()
        a1 = self.answer1Value.get()
        a2 = self.answer2Value.get()
        a3 = self.answer3Value.get()
        a4 = self.answer4Value.get()
        s = self.solutionValue.get()

        # create new Question: temp: 2 = solution
        newQuestion = Question()
        newQuestion.addQuestion(self.quizId, q, s, a1, a2, a3, a4, 60, 10)
        newQuestion.addQuestionToDatabase()
        newQuestion.getQuestionFromDatabase()

        # empty everything for new question
        # TO DO...


# screen HOST QUIZ
class HostQuizScreen(BaseScreen):
    # master = self from QuizApp
    def __init__(self, master, *args):

        # extend from BaseScreen
        BaseScreen.__init__(self, master)
        self.master = master

        if args:
            self.getArguments(*args)

        #layout
        self.configure(bg=self.setBackgroundColor())
        
        self.createLabel('Host Quiz', 'title').pack(side="top", fill="x", pady=30)

        self.createLabel('Enter your IP:', 'default').pack(side="top", fill="x", pady=5)

        self.ip = ""
        
        Entry(self, textvar=self.ip).pack()

        self.createLabel('Choose which quiz to host:', 'default').pack(side="top", fill="x", pady=5)

        self.showQuizes()

        self.createButton('Return', 'return', lambda: master.switch_frame(HomeScreen)).pack(side="top", fill="x",pady=20)

    def showQuizes(self):
        # show all quizes from database
        print('show quizes from database')

        q = Quiz()
        quizes = q.getDataFromDatabase()
        print(f'db: {quizes}')

        for item in quizes:
            quizId = item[0]
            self.createButton(item[1], 'default', lambda quizId=quizId: self.next(quizId)).pack(side="top",fill="x", pady=20)

    def next(self, quizId):
        ip = str(self.ip)
        server = Server(ip, 5000)

        print("this should be our quiz id -> "+str(quizId))
        q = Question()
        questions = q.createQuizWithQuestions(quizId)
        print("this should be a question list -> "+str(questions))
        
        server.setQuestionList(questions)
        self.master.switch_frame(HostQuizWaitingScreen, server)


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

        self.startServer()
        
        # layout
        self.configure(bg=self.setBackgroundColor())
        
        self.createLabel('Host Quiz', 'title').pack(side="top", fill="x", pady=30)
        
        self.waitingLabel = self.createLabel('Waiting for players...', 'default')
        self.waitingLabel.pack(side="top", fill="x", pady=5)
        
        self.playersLabel = self.createLabel('f"{str(len(self.server.clients))} players are connected"', 'default')
        self.playersLabel.pack()

        self.continueButton = self.createButton('Enough players', 'default', lambda: self.stopThread())
        self.continueButton.pack()
        
        self.createButton('Return', 'return', lambda: master.switch_frame(HomeScreen)).pack(side="top", fill="x",pady=20)

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
                self.continueButton.config(text='Start Quiz', command=lambda: self.master.switch_frame(HostQuizScoreScreen, self.server, 0))
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

    def startServer(self):
        print("start server")
        self.server.host()

    def stopThread(self):
        # stop thread:
        print("stop thread")
        self.start = True


# screen HOST QUIZ START
class HostQuizScoreScreen(BaseScreen):
    # master = self from QuizApp
    def __init__(self, master, *args):

        # extend from BaseScreen
        BaseScreen.__init__(self, master)

        if args:
            self.getArguments(*args)

        self.server = self.args[0]

        self.configure(bg=self.setBackgroundColor())
        
        #at what question are we?
        if self.args[1] == 0:
            # If position is 0 this is the first question.
            position = self.args[1]
            self.createButton('Send the first question!', 'default', lambda: master.switch_frame(HostQuizQuestionScreen, self.server, position)).pack()
        else:
            position = self.args[1]
            # send scores to clients
            self.server.sendScores()
            # show scoreboard
            scores = self.server.getSortedScores()

            title = self.createLabel('Scoreboard:', 'title')
            title.pack(side="top", fill="x", pady=30)

            for player in scores:
                self.createLabel(str(player[0])+" - "+str(player[1]), 'default').pack(side="top", fill="x", pady=5)

            if self.args[1] == len(self.server.questionList):
                title.config(text="Final scores:")

                self.createLabel(f"The winner is {scores[0][0]}!", 'default').pack(side="top", fill="x", pady=5)
                if len(scores) > 1:
                    self.createLabel(f"{scores[1][0]} came in second.", 'default').pack(side="top", fill="x", pady=5)
                if len(scores) > 2:
                    self.createLabel(f"{scores[3][0]} came in third.", 'default').pack(side="top", fill="x", pady=5)
                self.createButton('End quiz', 'default', lambda: self.endQuiz()).pack()
            else:
                self.createButton('Send the next question!', 'default', lambda: master.switch_frame(HostQuizQuestionScreen, self.server, position)).pack()

    def endQuiz(self):
        self.server.endQuiz()
        self.master.switch_frame(HomeScreen)

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

        #layout
        self.configure(bg=self.setBackgroundColor())

        self.createLabel('current question:', 'default').pack(side="top", fill="x", pady=5)

        self.createLabel(self.server.questionList[self.position]["question"], 'title').pack(side="top", fill="x", pady=5)

        for item in self.server.questionList[self.position]["options"]:
            self.createLabel(self.server.questionList[self.position]["options"][item], 'default').pack(side="top", fill="x", pady=5)

        self.server.handleNextQuestion()
        
        label3 = self.createLabel('Players are answering...', 'default')
        label3.pack(side="top", fill="x", pady=5)

        if self.server.wait():
            label3.destroy()
            self.createButton('View scores', 'confirm', lambda: master.switch_frame(HostQuizScoreScreen, self.server, self.position+1)).pack()

# screen JOIN QUIZ NOT UPDATED LAYOUT
class JoinQuizScreen(BaseScreen):
    # master = self from QuizApp
    def __init__(self, master, *args):

        # extend from BaseScreen
        BaseScreen.__init__(self, master)

        if args:
            self.getArguments(*args)

        # input vars
        ipValue = ""
        usernameValue = "User"

        # layout
        self.configure(bg=self.setBackgroundColor())
        
        self.createLabel('Join Quiz', 'title').pack(side="top", fill="x", pady=30)
        
        self.createLabel('Enter ip', 'default').pack()
        Entry(self, textvar=ipValue).pack()

        self.createLabel('Enter nickname', 'default').pack()
        Entry(self, textvar=usernameValue).pack()

        client = Client(ipValue, 5000)
        client.setName(usernameValue)

        self.createButton('Join', 'default', lambda: master.switch_frame(JoinQuizConnectScreen, client)).pack(side="top", fill="x", pady=20)
        self.createButton('Return', 'return', lambda: master.switch_frame(HomeScreen)).pack()

class JoinQuizConnectScreen(BaseScreen):
    # master = self from QuizApp
    def __init__(self, master, *args):

        # extend from BaseScreen
        BaseScreen.__init__(self, master)

        if args:
            self.getArguments(*args)

        self.client = self.args[0]
        
        # layout
        self.configure(bg=self.setBackgroundColor())

        self.createLabel('Join Quiz', 'title').pack(side="top", fill="x", pady=30)

        connectingLabel = self.createLabel('Connecting to host', 'default')
        connectingLabel.pack()

        if self.client.join():
            connectingLabel.config(text="Connected!")
            self.createLabel('Waiting for the Quiz master to send the first Question', 'default').pack()
            #self.client.listen()
            #if self.client.getQuestion() != None:
                #master.switch_frame(HomeScreen).pack()
        else:
            connectingLabel.config(text="Failed to connect to host.")
            self.createButton('Return', 'return', lambda: master.switch_frame(HomeScreen)).pack()

class JoinQuizQuestionScreen(BaseScreen):
    # master = self from QuizApp
    def __init__(self, master, *args):

        # extend from BaseScreen
        BaseScreen.__init__(self, master)

        if args:
            self.getArguments(*args)

        self.client = self.args[0]
        
        # layout
        self.configure(bg=self.setBackgroundColor())

        self.createLabel(self.client.getQuestion(), 'title').pack(side="top", fill="x", pady=30)

        
