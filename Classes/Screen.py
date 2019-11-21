import threading
import time
from tkinter import *
from Classes.Quiz import Quiz
from Classes.Question import Question
from Classes.Sockets import Server
from Classes.Sockets import Client

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
        self.buttonActiveBackColor = "#EDEDED"
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

    def createButton(self, text, type, method, *state):
        if state:
            print('test ' + str(text))
            arg = state[0]
            self.newState = arg
        else:
            self.newState = 'normal'

        # methods:
        # function or switch screen
        newMethod = method

        # type (basic,...), method: , colors:

        # CONFIRM button: bg green
        if type == "confirm":
            newButtonForeColor = "#FFF"
            newButtonBackColor = "green"
            newButtonActiveForeColor = "#FFF"
            newButtonActiveBackColor = "#5E9858"

            button = Button(self, text=text, fg=newButtonForeColor, bg=newButtonBackColor, state = self.newState,
                          activeforeground=newButtonActiveForeColor, activebackground=newButtonActiveBackColor,
                          relief=FLAT, width=self.buttonWidth, font=(self.buttonFontFamily, self.buttonFontSize, self.buttonFontType), command=method)


        # RETURN button bg red
        elif type == "return":
            newButtonForeColor = "#FFF"
            newButtonBackColor = "#92050C"
            newButtonActiveForeColor = "#FFF"
            newButtonActiveBackColor = "#B15943"

            button = Button(self, text=text, fg=newButtonForeColor, bg=newButtonBackColor, state = self.newState,
                            activeforeground=newButtonActiveForeColor, activebackground=newButtonActiveBackColor,
                            relief=FLAT, width=self.buttonWidth,
                            font=(self.buttonFontFamily, self.buttonFontSize, self.buttonFontType), command=method)

        # DEFAULT button
        elif type == "default":
            # default buttons, no vars to change
            button = Button(self, text=text, fg=self.buttonForeColor, bg=self.buttonBackColor, state = self.newState,
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

        self.saveButton = self.createButton('Save', 'confirm', lambda: self.saveQuiz())
        self.saveButton.pack(side="top",fill="x",pady=10)

        self.returnButton = self.createButton('Return', 'return', lambda: master.switch_frame(HomeScreen))
        self.returnButton.pack(side="top",fill="x",pady=10)

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

        # change button
        self.saveButton.config(text='Add Questions',command=lambda: self.master.switch_frame(CreateQuestionScreen, createQuizId))
        # disable return button (you can't make an empty quiz)
        self.returnButton.destroy()


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
        self.questionInput = self.createInput(self.questionValue, 'default')
        self.questionInput.pack()


        self.createLabel('Answer 1', 'default').pack()
        self.answer1Input = self.createInput(self.answer1Value, 'default')
        self.answer1Input.pack()

        self.createLabel('Answer 2', 'default').pack()
        self.answer2Input = self.createInput(self.answer2Value, 'default')
        self.answer2Input.pack()

        self.createLabel('Answer 3', 'default').pack()
        self.answer3Input = self.createInput(self.answer3Value, 'default')
        self.answer3Input.pack()

        self.createLabel('Answer 4', 'default').pack()
        self.answer4Input = self.createInput(self.answer4Value, 'default')
        self.answer4Input.pack()

        # TO DO: LAYOUT
        solutionLabel = Label(self, text='Correct answer', fg='black', font=('arial', 16, 'bold')).pack()
        r1 = Radiobutton(self, text='1', variable=self.solutionValue, value='option1').pack()
        r2 = Radiobutton(self, text='2', variable=self.solutionValue, value='option2').pack()
        r3 = Radiobutton(self, text='3', variable=self.solutionValue, value='option3').pack()
        r4 = Radiobutton(self, text='4', variable=self.solutionValue, value='option4').pack()

        self.saveQuestionButton = self.createButton('Save Question', 'confirm', lambda: self.addQuestion())
        self.saveQuestionButton.pack(side="top", fill="x",pady=10)

        self.finishQuizButton = self.createButton('Finish Quiz', 'confirm', lambda: master.switch_frame(HostQuizScreen), 'disabled')
        self.finishQuizButton.pack(side="top", fill="x",pady=10)

    def addQuestion(self):
        # create new Quiz
        print(f'Quiz Id: {self.quizId}')

        q = self.questionValue.get()
        a1 = self.answer1Value.get()
        a2 = self.answer2Value.get()
        a3 = self.answer3Value.get()
        a4 = self.answer4Value.get()
        s = self.solutionValue.get()

        # create new Question:
        newQuestion = Question()
        newQuestion.addQuestion(self.quizId, q, s, a1, a2, a3, a4, 60, 10)
        newQuestion.addQuestionToDatabase()
        newQuestion.getQuestionFromDatabase()

        # empty everything for new question
        self.questionValue.set("")
        self.answer1Value.set("")
        self.answer2Value.set("")
        self.answer3Value.set("")
        self.answer4Value.set("")

        # change finish button from disabled to active
        self.finishQuizButton.config(state="normal")

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

        self.ip = StringVar()
        
        self.createInput(self.ip, 'default').pack()

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
        ip = self.ip.get()
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
        self.master = master

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
        
        self.status = self.createLabel('Players are answering...', 'default')
        self.status.pack(side="top", fill="x", pady=5)

        x = threading.Thread(target=self.sendQuestion).start()

    def sendQuestion(self):
        self.server.handleNextQuestion()

        if self.server.wait():
            self.status.destroy()
            self.createButton('View scores', 'confirm', lambda: self.master.switch_frame(HostQuizScoreScreen, self.server, self.position+1)).pack()

# screen JOIN QUIZ NOT UPDATED LAYOUT
class JoinQuizScreen(BaseScreen):
    # master = self from QuizApp
    def __init__(self, master, *args):

        # extend from BaseScreen
        BaseScreen.__init__(self, master)
        self.master = master

        if args:
            self.getArguments(*args)

        # input vars
        self.ipValue = StringVar()
        self.usernameValue = StringVar()

        # layout
        self.configure(bg=self.setBackgroundColor())
        
        self.createLabel('Join Quiz', 'title').pack(side="top", fill="x", pady=30)
        
        self.createLabel('Enter ip', 'default').pack()
        self.createInput(self.ipValue, 'default').pack()

        self.createLabel('Enter nickname', 'default').pack()
        self.createInput(self.usernameValue, 'default').pack()

        self.createButton('Join', 'default', lambda: self.join()).pack(side="top", fill="x", pady=20)
        self.createButton('Return', 'return', lambda: master.switch_frame(HomeScreen)).pack()

    def join(self):
        ip = self.ipValue.get()
        client = Client(ip, 5000)
        
        username = self.usernameValue.get()
        if username == "":
            username = "User"
        client.setName(username)

        self.master.switch_frame(JoinQuizConnectScreen, client)

class JoinQuizConnectScreen(BaseScreen):
    # master = self from QuizApp
    def __init__(self, master, *args):

        # extend from BaseScreen
        BaseScreen.__init__(self, master)
        self.master = master

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
            x = threading.Thread(target=self.receiveQuestion).start()
        else:
            connectingLabel.config(text="Failed to connect to host.")
            self.createButton('Return', 'return', lambda: master.switch_frame(HomeScreen)).pack()

    def receiveQuestion(self):
        self.createLabel('Waiting for the Quiz master to send the first Question', 'default').pack()
        self.client.listen()
        print("done listening")
        if self.client.getQuestion() != None:
            self.master.switch_frame(JoinQuizQuestionScreen, self.client)

class JoinQuizQuestionScreen(BaseScreen):
    # master = self from QuizApp
    def __init__(self, master, *args):

        print("1")

        # extend from BaseScreen
        BaseScreen.__init__(self, master)

        if args:
            self.getArguments(*args)

        self.client = self.args[0]
        self.answered = False

        print("2")
        
        # layout
        self.configure(bg=self.setBackgroundColor())

        self.createLabel(self.client.getQuestion(), 'title').pack(side="top", fill="x", pady=30)


        print("3")
        options = self.client.getQuestionOptions()
        for option in options:
            self.createButton(options[option], 'default', lambda option=option: self.answer(option)).pack()
        
        if self.client.getTime() != None:
            x = threading.Thread(target=lambda: self.countdown(self.client.getTime())).start()
        print("4")
        
    def answer(self, option):
        if self.answered == False:
            self.client.answer(option)
            self.answered = True
            self.master.switch_frame(JoinQuizWaitingScreen, self.client)

    def countdown(self, seconds):

        print("countdown")
        
        timer = self.createLabel("Time: "+str(seconds), 'default')
        timer.pack()

        while self.answered == False:
            time.sleep(1)
            timer.config(text="Time: "+str(seconds))
            if seconds <= 0:
                self.client.answer(False)
                self.answered = True
                self.master.switch_frame(JoinQuizWaitingScreen, self.client, "timeout")
                break
            seconds = seconds - 1
        
class JoinQuizWaitingScreen(BaseScreen):
    # master = self from QuizApp
    def __init__(self, master, *args):

        # extend from BaseScreen
        BaseScreen.__init__(self, master)

        if args:
            self.getArguments(*args)

        self.client = self.args[0]

        # layout
        self.configure(bg=self.setBackgroundColor())

        if len(self.args) > 1 and self.args[1] == "timeout":
            self.createLabel("You didn't answer in time!", 'default').pack()
            self.createLabel('Waiting on Quiz host', 'default').pack()
        else:
            self.createLabel("Your answer was send.", 'default').pack()
            self.createLabel('Now waiting for other players to answer...', 'default').pack()
        
        x = threading.Thread(target=self.receiveScores).start()
        
    def receiveScores(self):
        self.client.listen()
        print("done listening")
        if self.client.getScores() != None:
            self.master.switch_frame(JoinQuizScoreScreen, self.client)
        
class JoinQuizScoreScreen(BaseScreen):
    # master = self from QuizApp
    def __init__(self, master, *args):

        # extend from BaseScreen
        BaseScreen.__init__(self, master)

        if args:
            self.getArguments(*args)

        self.client = self.args[0]
        
        # layout
        self.configure(bg=self.setBackgroundColor())

        scores = self.client.getScores()

        title = self.createLabel('Scoreboard:', 'title')
        title.pack(side="top", fill="x", pady=30)

        for player in scores:
            self.createLabel(str(player[0])+" - "+str(player[1]), 'default').pack(side="top", fill="x", pady=5)

        x = threading.Thread(target=self.receiveQuestion).start()
        
    def receiveQuestion(self):
        waitingMessage = self.createLabel('Get ready for the next question...', 'default')
        waitingMessage.pack()
        self.client.listen()
        print("done listening")
        if self.client.ended:
            self.master.switch_frame(JoinQuizEndScreen, self.client)
            
        elif self.client.getQuestion() != None:
            self.master.switch_frame(JoinQuizQuestionScreen, self.client)

class JoinQuizEndScreen(BaseScreen):        
    # master = self from QuizApp
    def __init__(self, master, *args):

        # extend from BaseScreen
        BaseScreen.__init__(self, master)

        if args:
            self.getArguments(*args)

        self.client = self.args[0]
        
        # layout
        self.configure(bg=self.setBackgroundColor())

        scores = self.client.getScores()

        if scores[0][0] == self.client.name:
            self.createLabel('You won! Congratulations!', 'title').pack()
        else:
            self.createLabel(f'{scores[0][0]} won!', 'title').pack()
        if (len(scores) >= 2) and (scores[1][0] == self.client.name):
            self.createLabel('You came in second!', 'default').pack()
        if (len(scores) >= 3) and (scores[2][0] == self.client.name):
            self.createLabel('You came in third!', 'default').pack()
        self.client.end()
        self.createButton('Return to home screen', 'confirm', lambda: master.switch_frame(HomeScreen)).pack()
        
