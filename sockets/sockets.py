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
        self.question = False #tells wether or not there is a question ready to be answered
    
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
                d = pickle.loads(full_msg[HEADERSIZE:])
                message = json.loads(d)
                return message


c = Client("",5000)

input("press enter to join")
c.join()

name = input("who are you?")
c.setName(name)
input("press enter to join")

