import socket
import pickle
import random
import json
import threading
import time
import sys

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
                    if 'time' in message:
                        x = threading.Thread(target=self.timer, args=([message['time']]))
                        x.start()
                    break
                if message["type"] == "scores":
                    self.newScores = message["scoreboard"]
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

    def answer(self, answer):
        if self.newQuestion != None:
            answer = answer.upper()
            if answer == False or answer == None or answer == "out of time":
                answer = '{"sender":"'+self.name+'", "answer":"out of time"}'
            elif answer == "A" or answer == "B" or answer == "C" or answer == "D":
                answer = '{"sender":"'+self.name+'", "answer":"'+answer+'"}'
            else:
                print("Please choose between A, B, C or D")
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

c = Client("",5000)

input("press enter to join")
c.join()

name = input("who are you?")
c.setName(name)
input("press enter to listen to the server")

c.listen()
print("done listening")
print(c.lastMessage)

print("press enter to see the question")
print(c.getQuestion())
print(c.getQuestionOptions())

print("the timer is:")
print(c.getTimer())

print("")
c.answer("a")


