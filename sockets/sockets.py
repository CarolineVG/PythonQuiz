import socket
import pickle
import random
import json
import threading
import time
import sys

class Server:
    def __init__(self, ip, port):
        #standard variables
        self.ip = ip
        if self.ip == "": #defaults to localhost if no ip was given
            self.ip = socket.gethostname()
        self.port = port
        self.headerSize = 10 #length of header before every send message, that specifies how long the whole message is

        #server variables
        self.access = True #can players (still) join the quiz?
        self.ready = False #are we complete or are we waiting on something?
        self.clients = set() #the players
        self.questionList = [] #list of questions. Saved here as a list of dictionaries
        self.currentQuestion = 0 #our progress into the quiz
        self.scores = {} #dictionary of scores
        self.answers = 0 #a counter that keeps track of how many clients have answered already. Resets with every new question.
        self.endMessage = "Thank you for playing this Quiz!"

    def host(self):
        self.access = True
        a = threading.Thread(target=self.connectClients)
        a.start()

    def connectClients(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.ip, self.port))
        s.listen(5)
        while True:
            clientsocket, address = s.accept()
            if self.access == False:
                #send back message to client so the client will close connection (I can't figure out how to do it from here)
                self.sendToClient(clientSocket, '{"type":"connection refused"}')
            else:
                self.clients.add(clientsocket)
            print(f"{len(self.clients)} players have connected.")
    
    def stopHosting(self):
        self.access = False
        print("")
        if len(self.clients)>=1:
            print("All players are in.")
            self.ready = True
        else:
            print("No players were found.")
            sys.exit(0)

    def sendToClient(self, client, json):
        message = pickle.dumps(json)
        message = bytes(f'{len(message):<{self.headerSize}}', "utf-8") + message
        client.send(message)

    def sendToAll(self, json):
        for c in self.clients:
            self.sendToClient(c, json)

    def sendQuestion(self, client, question):
        if 'score' in question:
            score = question['score']
        else:
            score = 10
        if 'time' in question:
            question = '{"type":"question", "sender": "Host", "question": "'+question['question']+'", "options":'+json.dumps(question['options'])+',"time":'+json.dumps(question['time'])+',"score":'+str(score)+'}'
        else:
            question = '{"type":"question", "sender": "Host", "question": "'+question['question']+'", "options":'+json.dumps(question['options'])+',"score":'+str(score)+'}'
        self.sendToClient(client, question)

    def updateScores(self, name, answer, solution, score):
        #check if the answer was correct
        if answer == solution:
            #check if client is already in the scores
            if name in self.scores:
                self.scores[name] = self.scores.get(name) + score
            else:
                self.scores[name] = score
        elif name not in self.scores:
            self.scores[name] = 0

    def sortScores(self, scores):
        top5 = []
        for record in scores:
            top5.append([record, scores[record]])
        top5.sort(key=lambda x: x[1], reverse=True)
        return top5

    def everyoneAnswered(self):
        if self.answers == len(self.clients):
            return True
        else:
            return False

    def receiveAnswer(self, client, solution):
        fullAnswer = b''
        newAnswer = True
        while True:
            response = client.recv(8)
            if newAnswer:
                answerLength = int(response[:self.headerSize])
                newAnswer = False

            fullAnswer += response
            if len(fullAnswer)-self.headerSize == answerLength:
                answer = pickle.loads(fullAnswer[self.headerSize:])
                answer = json.loads(answer)
                
                self.answers = self.answers + 1

                self.updateScores(answer["sender"], answer["answer"], solution, answer["score"])
                
                if self.everyoneAnswered():
                    #all players have answered.
                    
                    print(f"All players answered question {self.currentQuestion+1}")

                    
                    self.answers = 0
                    self.currentQuestion = self.currentQuestion + 1
                    self.ready = True
                return

    def getScores(self):
        return self.scores

    def getSortedScores(self):
        return sortScores(self.scores)

    def waitAndGetScores(self):
        if self.ready == False:
            print("waiting for the scores...")
        while True:
            if self.ready:
                return self.scores
            
    def waitAndGetSortedScores(self):
        if self.ready == False:
            print("waiting for the scores...")
        while True:
            if self.ready:
                return sortScores(self.scores)
                

    def sendScores(self):
        if self.lastQuestion():
            scoreboard = '{"type":"scores", "scoreboard":'+json.dumps(self.scores)+',"endMessage":"Thank you for playing!"}'
        else:
            scoreboard = '{"type":"scores", "scoreboard":'+json.dumps(self.scores)+'}'
        self.sendToAll(scoreboard)

    def waitAndSendScores(self):
        if self.ready == False:
            print("Waiting for the scores...")
        while True:
            if self.ready:
                print("Scores are in.")
                self.sendScores()
                return
    
    def nextQuestionThread(self, position, client):
        self.sendQuestion(client, self.questionList[position])
        self.receiveAnswer(client, self.questionList[position]['solution'])
        if self.ready:
            time.sleep(1)
            return
                
    def handleNextQuestion(self):
        if self.ready:
            self.ready = False
            print(f"sending question {self.currentQuestion+1}")
            for c in self.clients:
                x = threading.Thread(target=self.nextQuestionThread, args=(self.currentQuestion, c))
                x.start()
        else:
            print("Not ready! We're still waiting for all clients.")

    def setQuestionList(self, questionList):
        self.questionList = questionList
        
    def addQuestion(self, dictionary):
        self.questionList.append(dictionary)

    def lastQuestion(self):
        if self.currentQuestion == len(self.questionList)-1:
            return True
        else:
            return False

    def setEndMessage(self, string):
        self.endMessage = string
        
    def endQuiz(self): #send an end message to the other programs. They then do whatever they want with it.
        message = '{"type":"end", "scoreboard":'+json.dumps(self.scores)+', "endMessage":"'+self.endMessage+'"}'
        print(message)
        self.sendToAll(message)
        for c in self.clients:
            print(str(c))
            c.close()

class Client:
    def __init__(self, ip, port):
        #standard variables
        self.ip = ip
        if self.ip == "": #defaults to localhost if no ip was given
            self.ip = socket.gethostname()
        self.port = port
        self.headerSize = 10 #length of header before every send message, that specifies how long the whole message is

        #client variables
        self.server = None
        self.name = None #name of this client on the scoreboard
        self.lastMessage = None
        self.newQuestion = None
        self.newScores = None
        self.ended = False
        self.endMessage = None
    
    def join(self): #method for clients, may remove it later
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((self.ip, self.port))
        print("connected to a quiz host.")

    def setName(self, string): #now you may say that this method is completely useless, but I'll have you know that you smell and your mom is gay
        self.name = string

    def getName(self, string):
        return self.name

    def sortScores(self, scores):
        top5 = []
        for record in scores:
            top5.append([record, scores[record]])
        top5.sort(key=lambda x: x[1], reverse=True)
        return top5

    def listen(self):
        self.newQuestion = None
        self.newScores = None
        
        fullMessage = b''
        newMessage = True
        while True:
            message = self.server.recv(8)
            if newMessage:
                messageLength = int(message[:self.headerSize])
                newMessage = False

            fullMessage += message
                
            if len(fullMessage)-self.headerSize == messageLength:
                d = pickle.loads(fullMessage[self.headerSize:])
                message = json.loads(d)
                self.lastMessage = message

                if message["type"] == "connection refused":
                    print("You were too late. The quiz has already started without you.")
                    break
                if message["type"] == "question":
                    self.newQuestion = message
                    self.answered = False
                    break
                if message["type"] == "scores":
                    self.newScores = message["scoreboard"]
                    break
                if message["type"] == "end":
                    self.ended = True
                    self.newScores = message["scoreboard"]
                    self.endMessage = message["endMessage"]
                    break
                    
    def getQuestion(self):
        if self.newQuestion != None:
            return self.newQuestion["question"]
        else:
            print("No question was asked")
            return None

    def getQuestionOptions(self):
        if self.newQuestion != None:
            return self.newQuestion["options"]
        else:
            print("No question was asked")
            return None

    def getQuestionScore(self):
        if self.newQuestion != None:
            return self.newQuestion["score"]
        else:
            print("No question was asked")
            return None

    def answer(self, answer):
        if self.newQuestion != None:
            if answer == False or answer == None or answer == "out of time":
                answer = '{"sender":"'+self.name+'", "answer":"out of time", "score":'+str(self.getQuestionScore())+'}'
            elif answer == "option1" or answer == "option2" or answer == "option3" or answer == "option4":
                answer = '{"sender":"'+self.name+'", "answer":"'+answer+'", "score":'+str(self.getQuestionScore())+'}'
            else:
                print("Not an option")
                return
            answer = pickle.dumps(answer)
            answer = bytes(f'{len(answer):<{self.headerSize}}', "utf-8") + answer

            self.server.sendall(answer)

            self.newQuestion = None
        else:
            print("You couldn't answer. Either no question was asked or you were too late.")

    def getTimer(self):
        if self.newQuestion != None:
            if 'timer' in self.lastMessage:
                return self.newQuestion['timer']
            else:
                return None
        else:
            print("No question was asked")
            return None

    def getScores(self):
        if self.newScores != None:
            return self.sortScores(self.newScores)
        else:
            print("No scores have been send")
            return None

    def getYourScore(self):
        if self.newScores != None:
            return self.newScores.get(self.name)
        else:
            print("No scores have been send")
            return None

    def getEndMessage(self):
        return self.endMessage

    def end(self):
        self.server.close()

switch = input("Server? ")
if switch == "yes" or switch == "y":
    s = Server("",5000)
    s.host()
    input("press enter to stop hosting")
    s.stopHosting()

    s.setQuestionList([ #list of (for now hard-coded) questions that the clients will answer
        {
            'question': 'What is the first letter of the alphabet?',
            'options':{
                'option1':'A',
                'option2':'B',
                'option3':'C',
                'option4':'D'
            },
            'solution':'option1'
        },
        {
            'question': 'What colour is the sky?',
            'options':{
                'option1':'Green',
                'option2':'Red',
                'option3':'Blue',
                'option4':'brown'
            },
            'solution':'option3',
            'time':30,
            'score':20
        },
        {
            'question': 'Who is the best python programmer?',
            'options':{
                'option1':'Roel',
                'option2':'Caroline',
                'option3':'Santa Claus'
            },
            'solution':'option2',
            'score':5
        },
        {
            'question': 'What is the airspeed velocity of an unladen swallow?',
            'options':{
                'option1':'I don\'t know that.',
                'option2':'Blue!',
                'option3':'That depends. Is it an African swallow or a European one?'
            },
            'solution':'option3',
            'time':30
        },
        {
            'question': 'Was this a fun quiz?',
            'options':{
                'option1':'Yes!',
                'option2':'No.'
            },
            'solution':'option2'
        }
    ])

    s.handleNextQuestion()
    s.waitAndSendScores()

    s.handleNextQuestion()
    s.waitAndSendScores()

    s.handleNextQuestion()
    s.waitAndSendScores()

    s.endQuiz()

else:
    c = Client("",5000)

    input("press enter to join")
    c.join()

    name = input("who are you?")
    c.setName(name)
    input("press enter to listen to the server")

    c.listen()
    print("done listening")
    print(c.lastMessage)
    print(c.getQuestion())
    print(c.getQuestionOptions())

    print("the timer is:")
    print(c.getTimer())

    print("")
    c.answer("option1")
    
    print("listening")
    c.listen()
    print("done listening")
    print(c.getYourScore())
    print(c.getScores())


    c.listen()
    print("done listening")
    print(c.lastMessage)
    print(c.getQuestion())
    print(c.getQuestionOptions())
    print(c.getQuestionScore())

    print("the timer is:")
    print(c.getTimer())

    print("")
    c.answer("option3")
    
    print("listening")
    c.listen()
    print("done listening")
    print(c.getYourScore())
    print(c.getScores())


    c.listen()
    print("done listening")
    print(c.lastMessage)
    print(c.getQuestion())
    print(c.getQuestionOptions())
    print(c.getQuestionScore())

    print("the timer is:")
    print(c.getTimer())

    print("")
    c.answer("option2")
    
    print("listening")
    c.listen()
    print("done listening")
    print(c.getYourScore())
    print(c.getScores())

    
    print("listening")
    c.listen()
    print(c.ended)
    print(c.getYourScore())
    print(c.getScores())
    print(c.endMessage)
    c.end()

