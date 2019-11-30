import threading
import time
from tkinter import *
from Classes.Quiz import Quiz
from Classes.Question import Question
from Classes.Sockets import Server
from Classes.Sockets import Client

from scapy.all import *

# class QuizApp
class QuizApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        self.switch_frame(HomeScreen)
        self.configure(bg='#FE715B')

        # check size of screen
        height = self.winfo_screenheight()
        width = self.winfo_screenwidth()
        pixels = str(width - 10) + 'x' + str(height)
        self.geometry(pixels)

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
        # TITLE
        elif type == "heading1":
            newLabelFontSize = 22
            newLabelFontType = 'bold'

            label = Label(self, text=text, fg=self.labelForeColor, bg=self.labelBackColor,
                          font=(self.fontFamily, newLabelFontSize, newLabelFontType))
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

    def createRadioButton(self, text, variable, value):
        radio = Radiobutton(self, text=text, variable=variable, value=value, fg = self.labelForeColor, bg = self.labelBackColor,
                            activeforeground=self.labelForeColor, activebackground=self.labelBackColor, font=(self.fontFamily, self.labelFontSize, self.labelFontType))

        return radio

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
        self.createButton('Manage Quizes', 'default', lambda: master.switch_frame(ManageQuizesScreen)).pack(side="top",fill="x",pady=20)
        self.createButton('Host Quiz', 'default', lambda: master.switch_frame(HostQuizScreen, 'a')).pack(side="top",fill="x",pady=20)
        self.createButton('Play Quiz', 'default', lambda: master.switch_frame(JoinQuizScreen)).pack(side="top",fill="x",pady=20)


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

        self.createLabel('Quiz Name', 'default').pack(side="top", fill="x", pady=30)
        self.createInput(self.quizValue, 'default').pack()

        self.saveButton = self.createButton('Save', 'confirm', lambda: self.saveQuiz())
        self.saveButton.pack(side="top",fill="x",pady=10)

        self.returnButton = self.createButton('Return', 'return', lambda: master.switch_frame(HomeScreen))
        self.returnButton.pack(side="top",fill="x",pady=10)

        self.errorLabel = self.createLabel('', 'default')
        self.errorLabel.pack(side="top", fill="x", pady=30)

    def saveQuiz(self):
        # validation
        q = self.quizValue.get()
        if len(q) == 0 or q == None:
            print('empty')
            self.errorLabel.config(text='Please enter a quiz name')
        else:
            self.errorLabel.config(text='')

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

        self.questionValue = StringVar()
        self.answer1Value = StringVar()
        self.answer2Value = StringVar()
        self.answer3Value = StringVar()
        self.answer4Value = StringVar()
        self.solutionValue = StringVar()
        self.timerValue = StringVar()
        self.pointsValue = StringVar()

        # layout
        self.configure(bg=self.setBackgroundColor())

        self.createLabel('Quiz*', 'title').pack(side="top", fill="x", pady=30)

        self.createLabel('Question*', 'default').pack()
        self.questionInput = self.createInput(self.questionValue, 'default')
        self.questionInput.pack()

        self.createLabel('Answer 1*', 'default').pack()
        self.answer1Input = self.createInput(self.answer1Value, 'default')
        self.answer1Input.pack()

        self.createLabel('Answer 2*', 'default').pack()
        self.answer2Input = self.createInput(self.answer2Value, 'default')
        self.answer2Input.pack()

        self.createLabel('Answer 3', 'default').pack()
        self.answer3Input = self.createInput(self.answer3Value, 'default')
        self.answer3Input.pack()

        self.createLabel('Answer 4', 'default').pack()
        self.answer4Input = self.createInput(self.answer4Value, 'default')
        self.answer4Input.pack()

        self.createLabel('Correct Answer*', 'default').pack()
        self.createRadioButton('1', self.solutionValue, 'option1').pack()
        self.createRadioButton('2', self.solutionValue, 'option2').pack()
        self.createRadioButton('3', self.solutionValue, 'option3').pack()
        self.createRadioButton('4', self.solutionValue, 'option4').pack()

        self.createLabel('Timer*', 'default').pack()
        self.timerInput = self.createInput(self.timerValue, 'default')
        self.timerInput.pack()

        self.createLabel('Points*', 'default').pack()
        self.pointsInput = self.createInput(self.pointsValue, 'default')
        self.pointsInput.pack()

        self.saveQuestionButton = self.createButton('Save Question', 'confirm', lambda: self.addQuestion())
        self.saveQuestionButton.pack(side="top", fill="x",pady=10)

        self.finishQuizButton = self.createButton('Finish Quiz', 'confirm', lambda: master.switch_frame(HostQuizScreen), 'disabled')
        self.finishQuizButton.pack(side="top", fill="x",pady=10)

        self.errorLabel = self.createLabel('', 'default')
        self.errorLabel.pack(side="top", fill="x", pady=30)

    def addQuestion(self):
        # create new Quiz
        print(f'Quiz Id: {self.quizId}')

        q = self.questionValue.get()
        a1 = self.answer1Value.get()
        a2 = self.answer2Value.get()
        a3 = self.answer3Value.get()
        a4 = self.answer4Value.get()
        s = self.solutionValue.get()
        t = self.timerValue.get()
        p = self.pointsValue.get()

        # validation
        values = [q, a1, a2, s, t, p]
        emptyFields = False
        for v in values:
            if len(v) == 0 or v is None:
                print('empty')
                self.errorLabel.config(text='Please enter required fields')
                emptyFields = True

        if emptyFields == False:
            self.errorLabel.config(text='')

            # create new Question:
            newQuestion = Question()
            newQuestion.addQuestion(self.quizId, q, s, a1, a2, a3, a4, int(t), int(p))
            newQuestion.addQuestionToDatabase()
            newQuestion.getQuestionFromDatabase()

            # empty everything for new question
            self.questionValue.set("")
            self.answer1Value.set("")
            self.answer2Value.set("")
            self.answer3Value.set("")
            self.answer4Value.set("")
            self.timerValue.set("")
            self.pointsValue.set("")

            # change finish button from disabled to active
            self.finishQuizButton.config(state="normal")


# screen MANAGE QUIZES
class ManageQuizesScreen(BaseScreen):
    # master = self from QuizApp
    def __init__(self, master, *args):

        # extend from BaseScreen
        BaseScreen.__init__(self, master)
        self.master = master

        if args:
            self.getArguments(*args)

        # layout
        self.configure(bg=self.setBackgroundColor())

        self.createLabel('Manage Quizes', 'title').pack(side="top", fill="x", pady=30)

        self.showQuizes()

        self.createButton('Return', 'return', lambda: master.switch_frame(HomeScreen)).pack(side="top", fill="x", pady=20)

    def showQuizes(self):
        # show all quizes from database
        print('show quizes from database')

        q = Quiz()
        quizes = q.getDataFromDatabase()
        print(f'db: {quizes}')

        for item in quizes:
            quizId = item[0]
            self.createLabel(item[1], 'heading1').pack()
            self.createButton('Delete', 'return', lambda quizId=quizId: self.deleteQuiz(quizId)).pack(side="top", fill="x",
                                                                                                pady=5)

    def deleteQuiz(self, quizId):
        # delete quiz to do

        # db delete: quiz
        quiz = Quiz()
        quiz.deleteQuiz(quizId)

        # db delete: question
        question = Question()
        question.deleteQuestion(quizId)

        # refresh screen
        self.master.switch_frame(ManageQuizesScreen)


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

        # get IP from pc
        self.ipFromWifi = self.getIpFromPc()
        
        ipLabel = self.createInput(self.ip, 'default')
        ipLabel.pack()
        ipLabel.insert(0, self.ipFromWifi)

        self.createLabel('Choose which quiz to host:', 'default').pack(side="top", fill="x", pady=5)

        self.showQuizes()

        self.createButton('Return', 'return', lambda: master.switch_frame(HomeScreen)).pack(side="top", fill="x",pady=20)

    def getIpFromPc(self):
        print('f')
        # TRY: get IP from pc
        result = get_windows_if_list()
        print(result)
        for r in result:
            if r['name'] == 'WiFi' or r["name"] == "Wi-Fi":
                ipAddress = r['ips'][1]
            else:
                print("wifi wasn't found")
        return ipAddress

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
        print(ip)
        server = Server(ip, 5000)

        print("this should be our quiz id -> "+str(quizId))
        q = Question()
        questions = q.createQuizWithQuestions(quizId)
        print("this should be a question list -> "+str(questions))

        server.setQuestionList(questions)
        self.master.switch_frame(HostQuizWaitingScreen, server)


# screen WAITING QUIZ
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
        self.cancel = False

        self.startServer()
        
        # layout
        self.configure(bg=self.setBackgroundColor())
        
        self.createLabel('Host Quiz', 'title').pack(side="top", fill="x", pady=30)
        
        self.waitingLabel = self.createLabel('Waiting for players...', 'default')
        self.waitingLabel.pack(side="top", fill="x", pady=5)
        
        self.playersLabel = self.createLabel('f"{str(len(self.server.clients))} players are connected"', 'default')
        self.playersLabel.pack()

        self.continueButton = self.createButton('Enough players', 'confirm', lambda: self.stopThread())
        self.continueButton.pack()
        
        self.createButton('Cancel', 'return', self.cancelQuiz).pack(side="top", fill="x",pady=20)
        
        x = threading.Thread(target=self.updateInterface).start()

    def cancelQuiz(self):
        if self.start:
            self.server.endQuiz()
            self.master.switch_frame(HomeScreen)
        else:
            self.cancel = True

    def updateInterface(self):        
        while True:
            if self.start:
                self.server.stopHosting()
                server = self.server
                # if there are no players, the quiz can't begin
                if len(self.server.clients) < 1:
                    self.waitingLabel.config(text = "No players were found!")
                    self.playersLabel.config(text="You need to find players to start the quiz...")
                    self.server.endQuiz()
                    self.continueButton.destroy()
                    break
                else:
                    self.continueButton.config(text='Start Quiz', command=lambda: self.master.switch_frame(HostQuizScoreScreen, self.server, 0))
                    self.waitingLabel.config(text = "Ready to begin")
                    break
            elif self.cancel:
                self.server.stopHosting()
                self.server.endQuiz()
                self.master.switch_frame(HomeScreen)
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


# screen HOST QUIZ START
class HostQuizScoreScreen(BaseScreen):
    # master = self from QuizApp
    def __init__(self, master, *args):

        # extend from BaseScreen
        BaseScreen.__init__(self, master)

        if args:
            self.getArguments(*args)

        self.server = self.args[0]

        # layout
        self.configure(bg=self.setBackgroundColor())

        self.createLabel('Host Quiz', 'title').pack(side="top", fill="x", pady=30)
        
        if self.args[1] == 0:
            # first question
            position = self.args[1]
            self.sendQuestionButton = self.createButton('Send First Question', 'confirm', lambda: master.switch_frame(HostQuizQuestionScreen, self.server, position))
            self.sendQuestionButton.pack()
        else:
            # score
            self.showScore()

    def showScore(self):
        position = self.args[1]
        # send scores to clients
        self.server.sendScores()
        # show scoreboard
        scores = self.server.getSortedScores()

        # layout
        title = self.createLabel('Scoreboard', 'heading1')
        title.pack(side="top", fill="x", pady=5)

        for player in scores:
            self.createLabel(str(player[0])+" - "+str(player[1]) + " points", 'default').pack(side="top", fill="x", pady=5)

        if self.args[1] == len(self.server.questionList):
            title.config(text="Final scores:")

            self.createLabel(f"The winner is {scores[0][0]}!", 'default').pack(side="top", fill="x", pady=5)
            if len(scores) > 1:
                self.createLabel(f"{scores[1][0]} came in second.", 'default').pack(side="top", fill="x", pady=5)
            if len(scores) > 2:
                self.createLabel(f"{scores[3][0]} came in third.", 'default').pack(side="top", fill="x", pady=5)
            self.createButton('End quiz', 'confirm', lambda: self.endQuiz()).pack()
        else:
            self.createButton('Send the next question!', 'confirm', lambda: self.master.switch_frame(HostQuizQuestionScreen, self.server, position)).pack()

    def endQuiz(self):
        self.server.endQuiz()
        self.master.switch_frame(HomeScreen)


# screen HOST QUIZ QUESTION
class HostQuizQuestionScreen(BaseScreen):
    # master = self from QuizApp
    def __init__(self, master, *args):

        # extend from BaseScreen
        BaseScreen.__init__(self, master)
        self.master = master

        if args:
            self.getArguments(*args)

        self.server = self.args[0]
        
        self.position = self.args[1]

        # layout
        self.configure(bg=self.setBackgroundColor())

        self.createLabel('Host Quiz', 'title').pack(side="top", fill="x", pady=30)

        self.createLabel('Current Question', 'heading1').pack(side="top", fill="x", pady=5)

        self.createLabel(self.server.questionList[self.position]["question"], 'default').pack(side="top", fill="x", pady=5)

        self.createLabel('Answers', 'heading1').pack(side="top", fill="x", pady=5)

        # show answers
        for item in self.server.questionList[self.position]["options"]:
            self.createLabel('- ' + str(self.server.questionList[self.position]["options"][item]), 'default').pack(side="top", fill="x", pady=5)
            
        self.status = self.createLabel('Players are answering...', 'default')
        self.status.pack(side="top", fill="x", pady=30)

        x = threading.Thread(target=self.sendQuestion).start()
        self.done = False
        self.timeOut = False
        x = threading.Thread(target=self.timer).start()
            
    def sendQuestion(self):
        self.server.handleNextQuestion()
        
        if self.server.wait() and self.timeOut == False:
            self.status.destroy()
            self.done = True
            self.createButton('View scores', 'confirm', lambda: self.master.switch_frame(HostQuizScoreScreen, self.server, self.position+1)).pack(side="top", fill="x", pady=20)

    def timer(self):
        while self.done != True:
            if len(self.server.clients) < 1:
                self.timeOut = True
                self.master.switch_frame(HostQuizDisconnectScreen, self.server)
                break
        
class HostQuizDisconnectScreen(BaseScreen):
    # master = self from QuizApp
    def __init__(self, master, *args):

        # extend from BaseScreen
        BaseScreen.__init__(self, master)
        self.master = master

        if args:
            self.getArguments(*args)

        # var server
        self.server = self.args[0]

        #layout
        self.configure(bg=self.setBackgroundColor())
        
        self.createLabel('Host Quiz', 'title').pack(side="top", fill="x", pady=30)

        self.createLabel("It appears all players have dropped out.", "default").pack(side="top", fill="x", pady=5)

        self.createButton('Back to menu', 'return', lambda: self.master.switch_frame(HomeScreen)).pack(side="top", fill="x", pady=20)
        

# screen JOIN QUIZ
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


# screen JOIN QUIZ CONNECT
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
        self.createLabel('Waiting for the quiz master to send the first question', 'default').pack()
        self.client.listen()
        print("done listening")
        if self.client.ended:
            self.master.switch_frame(JoinQuizDisconnectScreen, self.client)
        if self.client.getQuestion() != None:
            self.master.switch_frame(JoinQuizQuestionScreen, self.client)

class JoinQuizDisconnectScreen(BaseScreen):
    # master = self from QuizApp
    def __init__(self, master, *args):

        # extend from BaseScreen
        BaseScreen.__init__(self, master)

        if args:
            self.getArguments(*args)

        self.client = self.args[0]

        self.client.end()

        #layout
        self.configure(bg=self.setBackgroundColor())
        self.createLabel('Disconnected', 'title').pack(side="top", fill="x", pady=30)
        self.createLabel('The host has canceled the quiz.', 'default').pack()
        self.createButton('Return', 'return', lambda: master.switch_frame(HomeScreen)).pack(side="top",pady=30)

# screen JOIN QUIZ QUESTION
class JoinQuizQuestionScreen(BaseScreen):
    # master = self from QuizApp
    def __init__(self, master, *args):

        # extend from BaseScreen
        BaseScreen.__init__(self, master)

        if args:
            self.getArguments(*args)

        self.client = self.args[0]
        self.answered = False
        
        # layout
        self.configure(bg=self.setBackgroundColor())

        self.createLabel('Play Quiz', 'title').pack(side="top", fill="x", pady=30)

        self.createLabel(f'{self.client.getQuestion()} ({self.client.getQuestionScore()} points)', 'heading1').pack(side="top", fill="x", pady=5)

        options = self.client.getQuestionOptions()
        for option in options:
            self.createButton(options[option], 'default', lambda option=option: self.answer(option)).pack(side="top", fill="x", pady=20)
        
        if self.client.getTime() != None:
            x = threading.Thread(target=lambda: self.countdown(self.client.getTime())).start()
        
    def answer(self, option):
        if self.answered == False:
            self.client.answer(option)
            self.answered = True
            self.master.switch_frame(JoinQuizWaitingScreen, self.client)

    def countdown(self, seconds):
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


# screen JOIN QUIZ WAITING
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

        self.createLabel('Play Quiz', 'title').pack(side="top", fill="x", pady=30)


        if len(self.args) > 1 and self.args[1] == "timeout":
            self.createLabel("You didn't answer in time!", 'default').pack()
            self.createLabel('Waiting on Quiz host', 'default').pack()
        else:
            self.createLabel("Your answer was sent.", 'default').pack()
            self.createLabel('Please wait for other players to answer...', 'default').pack()
        
        x = threading.Thread(target=self.receiveScores).start()
        
    def receiveScores(self):
        self.client.listen()
        print("done listening")
        if self.client.getScores() != None:
            self.master.switch_frame(JoinQuizScoreScreen, self.client)


# screen JOIN QUIZ SCORE
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

        self.createLabel('Play Quiz', 'title').pack(side="top", fill="x", pady=30)

        self.createLabel('The answer was:', 'heading1').pack(side="top", fill="x", pady=5)
        answer = self.client.getSolution()
        self.createLabel(answer, 'default').pack(side="top", fill="x", pady=5)

        self.createLabel('Scoreboard:', 'heading1').pack(side="top", fill="x", pady=5)

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


# screen JOIN QUIZ END
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
            self.createLabel('Play Quiz', 'title').pack(side="top", fill="x", pady=30)
            self.createLabel('You won! Congratulations!', 'heading1').pack(side="top", fill="x", pady=5)
        else:
            self.createLabel('Play Quiz', 'title').pack(side="top", fill="x", pady=30)
            self.createLabel(f'{scores[0][0]} won!', 'heading1').pack(side="top", fill="x", pady=5)
        if (len(scores) >= 2) and (scores[1][0] == self.client.name):
            self.createLabel('Play Quiz', 'title').pack(side="top", fill="x", pady=30)
            self.createLabel('You came in second!', 'default').pack()
        if (len(scores) >= 3) and (scores[2][0] == self.client.name):
            self.createLabel('Play Quiz', 'title').pack(side="top", fill="x", pady=30)
            self.createLabel('You came in third!', 'default').pack()
        self.client.end()
        self.createButton('Return to home screen', 'confirm', lambda: master.switch_frame(HomeScreen)).pack()
