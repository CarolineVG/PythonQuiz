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

    def join(self): #method for clients, may remove it later
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, self.port))
        print("connected to a quiz host.")

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
                sendToClient(clientSocket, '{"type":"connection refused"}')
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
        if 'time' in question:
            question = '{"type":"question", "sender": "Host", "id":"'+question['id']+'", "question": "'+question['question']+'", "options":'+json.dumps(question['options'])+',"time":'+json.dumps(question['time'])+'}'
        else:
            question = '{"type":"question", "sender": "Host", "id":"'+question['id']+'", "question": "'+question['question']+'", "options":'+json.dumps(question['options'])+'}'
        self.sendToClient(client, question)

    def updateScores(self, name, answer, solution):
        #check if the answer was correct
        if answer == solution:
            #check if client is already in the scores
            if name in self.scores:
                self.scores[name] = self.scores.get(name) + 1
            else:
                self.scores[name] = 1
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

                self.updateScores(answer["sender"], answer["answer"], solution)
                
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
            print("Everyone has answered")
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
        self.questionList.append(question)

    def lastQuestion(self):
        if self.currentQuestion == len(self.questionList)-1:
            return True
        else:
            return False

    '''
    TO DO:
        A method that ends the quiz. (this required changes on the client side too)
    '''

SERVER_IP = input("Enter your local IP: ")
if SERVER_IP == "":
    SERVER_IP = socket.gethostname() #localhost

server = Server(SERVER_IP, 5000)

server.host()

when = input("Listening for players...\nPress enter when enough players have joined.\n\n") #say when
if when != None:
    server.stopHosting()

server.setQuestionList([ #list of (for now hard-coded) questions that the clients will answer
        {
            'id': '0001',
            'question': 'What is the first letter of the alphabet?',
            'options':{
                'A':'A',
                'B':'B',
                'C':'C',
                'D':'D'
            },
            'solution':'A'
        },
        {
            'id': '0002',
            'question': 'What colour is the sky?',
            'options':{
                'A':'Green',
                'B':'Red',
                'C':'Blue',
                'D':'brown'
            },
            'solution':'C',
            'time':30
        },
        {
            'id': '0003',
            'question': 'Who is the best python programmer?',
            'options':{
                'A':'Roel',
                'B':'Caroline',
                'C':'Santa Claus'
            },
            'solution':'B'
        },
        {
            'id': '0004',
            'question': 'What is the airspeed velocity of an unladen swallow?',
            'options':{
                'A':'I don\'t know that.',
                'B':'Blue!',
                'C':'That depends. Is it an African swallow or a European one?'
            },
            'solution':'C',
            'time':30
        },
        {
            'id': '0005',
            'question': 'Was this a fun quiz?',
            'options':{
                'A':'Yes!',
                'B':'No.'
            },
            'solution':'B'
        }
    ])

server.handleNextQuestion()
server.waitAndSendScores()

while True:
    tuut = input("press enter to send the next question...")
    
    server.handleNextQuestion()
    server.waitAndSendScores()
    if server.lastQuestion():
        print("This was the last question")
    
