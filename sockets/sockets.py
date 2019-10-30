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
        self.ready = False #are we complete and ready to start?
        self.clients = set() #the players
        self.questionList = [] #list of questions. Saved here as a list of dictionaries
        self.currentQuestion #our progress into the quiz

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

    def sendToClient(client, json):
        message = pickle.dumps(json)
        message = bytes(f'{len(message):<{HEADERSIZE}}', "utf-8") + message
        client.send(message)

    def startQuiz():
        if self.ready:
            for c in self.clients:
                print("floep")
                #x = threading.Thread(target=handleQuiz, args=(c, questions))
                #x.start()
        else:
            print("Not ready yet. First we need to connect to all players.")

    def sendQuestion(self, client, question):
        solution = question['solution']
        if 'time' in question:
            question = '{"type":"question", "sender": "Host", "id":"'+question['id']+'", "question": "'+question['question']+'", "options":'+json.dumps(question['options'])+',"time":'+json.dumps(question['time'])+'}'
        else:
            question = '{"type":"question", "sender": "Host", "id":"'+question['id']+'", "question": "'+question['question']+'", "options":'+json.dumps(question['options'])+'}'
        self.sendToClient(client, question)

    def receiveAnswer():
        fullAnswer = b''
        newAnswer = True
        while True:
            response = clientsocket.recv(8)
            if newAnswer:
                answerLength = int(response[:HEADERSIZE])
                newAnswer = False

            fullAnswer += response
            if len(fullAnswer)-HEADERSIZE == answerLength:
                answer = pickle.loads(fullAnswer[HEADERSIZE:])
                answer = json.loads(answer)
                
                global answers
                answers = answers + 1

                #check if the answer was correct
                if answer["answer"] == solution:
                    #check if client is already in the scores
                    if answer["sender"] in scores:
                        scores[answer["sender"]] = scores.get(answer["sender"]) + 1
                    else:
                        scores[answer["sender"]] = 1
                elif answer["sender"] not in scores:
                    scores[answer["sender"]] = 0
                if answers == len(clients):
                    self.questionList
                    self.currentQuestion
                    if self.currentQuestion == len(self.questionList)-1:
                        scoreboard = '{"type":"scores", "scoreboard":'+json.dumps(scores)+',"endMessage":"Thank you for playing!"}'
                    else:
                        scoreboard = '{"type":"scores", "scoreboard":'+json.dumps(scores)+'}'
                    sendToAll(scoreboard)
                    print(f"All players answered question {currentQuestion+1}")

                    top5 = sortScores(scores)

                    print("")
                    print("Current scoreboard:")
                    print(f" - 1: {top5[0][1]} - {top5[0][0]}")
                    if len(top5) >= 2:
                        print(f" - 2: {top5[1][1]} - {top5[1][0]}")
                    if len(top5) >= 3:
                        print(f" - 3: {top5[2][1]} - {top5[2][0]}")
                    if len(top5) >= 4:
                        print(f" - 4: {top5[3][1]} - {top5[3][0]}")
                    if len(top5) >= 5:
                        print(f" - 5: {top5[4][1]} - {top5[4][0]}")
                    print("")
                    
                    answers = 0
                    currentQuestion = currentQuestion + 1
                return

    def setQuestionList(self, questionList):
        self.questionList = questionList
        
    def addQuestion(self, dictionary):
        self.questionList.append(question)
        

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



