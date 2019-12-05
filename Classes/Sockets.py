import socket
import pickle
import json
import threading
import time

class Server: #to be used in the GUI of the quiz master
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

    def host(self): #sets access to True and starts a new thread where connections with clients are made (connectClients())
        self.access = True
        a = threading.Thread(target=self.connectClients)
        a.start()

    def connectClients(self): #checks for a new connection every 0.5 seconds.
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.ip, self.port))
        s.listen(5)
        s.setblocking(0) #We use blocking sockets, but in the case of s.accept() it should be non-blocking so this thread can be closed down
        while True:
            if self.access == True:
                try:
                    clientsocket, address = s.accept()
                    if self.access == False:
                        #send back message to client so the client will close connection
                        #since this part was edited to be non-blocking this barely happens anymore
                        self.sendToClient(clientsocket, '{"type":"connection refused"}')
                    else:
                        clientsocket.setblocking(1) # for the rest of the program blocking sockets are fine, so we're setting it back to default for all client connections
                        self.clients.add(clientsocket)
                    print(f"{len(self.clients)} players have connected.")
                except:
                    print("checking for connections...")
                    time.sleep(0.5)
            else:
                print("hosting is stopped")
                break
    
    def stopHosting(self): #shut down the connectClients() thread by setting access to False, and check if we've found any players
        self.access = False
        print("")
        if len(self.clients)>=1:
            print("All players are in.")
            self.ready = True
        else:
            print("No players were found.")

    def sendToClient(self, client, json): #accepts a json string an sends it to a single client
        message = pickle.dumps(json)
        #print(message)
        message = bytes(f'{len(message):<{self.headerSize}}', "utf-8") + message
        try:
            client.send(message)
        except: #in case of a disconnected client an exception could occur here. This needs to be detected so the program never waits for a client that is no longer there.
            print("a client has disconnected (scenario 1)")
            #remove this player from the set
            client.close()
            self.clients.remove(client)

    def sendToAll(self, json): #accepts a json string and sends it to all clients
        for c in self.clients:
            self.sendToClient(c, json)

    def sendQuestion(self, client, question): #sends a question (a dictionary) to a single client
        if 'score' in question:
            score = question['score']
        else:
            score = 10
        if 'time' in question:
            question = '{"type":"question", "sender": "Host", "question": "'+question['question']+'", "options":'+json.dumps(question['options'])+',"time":'+json.dumps(question['time'])+',"score":'+str(score)+'}'
        else:
            question = '{"type":"question", "sender": "Host", "question": "'+question['question']+'", "options":'+json.dumps(question['options'])+',"score":'+str(score)+'}'
        self.sendToClient(client, question)

    def updateScores(self, name, answer, solution, score): #accepts a name, their answer, the correct answer, and the score the question is worth. Updates the scores if the player answered correctly
        #check if the answer was correct
        if answer == solution:
            #check if client is already in the scores
            if name in self.scores:
                self.scores[name] = self.scores.get(name) + score
            else:
                self.scores[name] = score
        elif name not in self.scores:
            self.scores[name] = 0

    def sortScores(self, scores): #returns a sorted list of scores
        top = []
        for record in scores:
            top.append([record, scores[record]])
        top.sort(key=lambda x: x[1], reverse=True)
        return top

    def everyoneAnswered(self): #just checks if everyone has answered the latest question or not
        if self.answers == len(self.clients):
            return True
        else:
            return False

    def receiveAnswer(self, client, solution): #receives an answer from a client.
        fullAnswer = b''
        newAnswer = True
        while True:
            try:
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
                    
                    if self.everyoneAnswered(): #if this is the last client that has answered, the server is ready to continue with the quiz.
                        #all players have answered.
                        self.answers = 0
                        self.currentQuestion = self.currentQuestion + 1
                        self.ready = True
                    return
            except: #in case of a disconnected client an exception could occur here. This needs to be detected so the program never waits for a client that is no longer there.
                print("a client has disconnected (scenario 2)")
                #remove this player from the set.
                client.close()
                self.clients.remove(client)
                #check if everyone has answered
                print("len in Sockets.py scenario 2 = "+str(len(self.clients)))
                if len(self.clients) > 0 and self.everyoneAnswered():
                    self.answers = 0
                    self.currentQuestion = self.currentQuestion + 1
                    self.ready = True
                return

    def getScores(self):
        return self.scores

    def getSortedScores(self):
        return self.sortScores(self.scores)

    def wait(self): #pause the current thread untill the server is ready
        if self.ready == False:
            print("waiting...")
        while True:
            if self.ready:
                print("waiting is over")
                return True
            
    def waitAndGetScores(self): #pause the current thread untill the server is ready, then return scores
        self.wait()
        return self.scores
            
    def waitAndGetSortedScores(self): #pause the current thread untill the server is ready, then return scores in a sorted list
        self.wait()
        return sortScores(self.scores)

    def sendScores(self): #send the scores to all clients
        solution = self.questionList[self.currentQuestion-1]["options"][self.questionList[self.currentQuestion-1]["solution"]]
        if self.lastQuestion():
            scoreboard = '{"type":"scores", "solution":"'+solution+'", "scoreboard":'+json.dumps(self.scores)+',"endMessage":"Thank you for playing!"}'
        else:
            scoreboard = '{"type":"scores", "solution":"'+solution+'", "scoreboard":'+json.dumps(self.scores)+'}'
        self.sendToAll(scoreboard)

    def waitAndSendScores(self): #pause the current thread untill the server is ready, then send the scores to all clients
        self.wait()
        print("Scores are in.")
        self.sendScores()
    
    def nextQuestionThread(self, position, client): #will send a question to a client, then receive their answer
        self.sendQuestion(client, self.questionList[position])
        self.receiveAnswer(client, self.questionList[position]['solution'])
                
    def handleNextQuestion(self): #will send the next question (depending on self.currentQuestion) to all clients, then receive all the answers. One thread per client is created.
        if self.ready:
            self.ready = False
            print(f"sending question {self.currentQuestion+1}")
            for c in self.clients:
                x = threading.Thread(target=self.nextQuestionThread, args=(self.currentQuestion, c))
                x.start()
        else:
            print("Not ready! We're still waiting for all clients.")

    def setQuestionList(self, questionList): #accepts a list of dictionaries
        self.questionList = questionList
        
    def addQuestion(self, dictionary): #accepts a dictionary
        self.questionList.append(dictionary)

    def lastQuestion(self): #checks if we are at the last question or not. Returns True or False
        if self.currentQuestion == len(self.questionList)-1:
            return True
        else:
            return False

    def setEndMessage(self, string): #sets the end message of the quiz (turns out we don't use end messages, but oh well)
        self.endMessage = string

    def getCurrentTimer(self): #get the timer of the current question (total amount of time a player gets to answer)
        return self.questionList[self.currentQuestion]["time"]
        
    def endQuiz(self): #send a message to the clients telling them the server has closed down. They then do whatever they want with it.
        message = '{"type":"end", "scoreboard":'+json.dumps(self.scores)+', "endMessage":"'+self.endMessage+'"}'
        self.sendToAll(message)
        print("disconnecting all client sockets")
        for c in self.clients:
            c.close()
        print("done.")



class Client: #to be used in the GUI of players
    def __init__(self, ip, port):
        #standard variables
        self.ip = ip
        if self.ip == "": #defaults to localhost if no ip was given
            self.ip = socket.gethostname()
        self.port = port
        self.headerSize = 10 #length of header before every send message, that specifies how long the whole message is

        #client variables
        self.server = None #the server socket
        self.name = None #name of this client on the scoreboard
        self.lastMessage = None # the last message the server has send
        self.newQuestion = None # the last question the server has send. If the server has send no question you haven't answered yes, this will be None
        self.newScores = None # the last scores the server has send
        self.ended = False #this variable helps to check in the GUI if the quiz has ended or not
        self.endMessage = None
        self.solution = None #the correct answer to the last question you answered
    
    def join(self): #connect to a server
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.connect((self.ip, self.port))
            print("connected to a quiz host.")
            return True
        except:
            print("failed to connect.")
            return False

    def setName(self, string):
        self.name = string

    def getName(self, string):
        return self.name

    def sortScores(self, scores): #convert the received scores to a sorted list
        top = []
        for record in scores:
            top.append([record, scores[record]])
        top.sort(key=lambda x: x[1], reverse=True)
        return top

    def listen(self): #wait for a new message from the server and get all required information when it arrives
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
                    self.solution = message["solution"]
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

    def answer(self, answer): #send an answer to the server. It is possible to put False, None or "out of time" as answer for when the user was too late to answer
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

    def getTime(self): #returns the time in which the current question needs to be answered. Integer
        if self.newQuestion != None:
            if 'time' in self.lastMessage:
                return self.newQuestion['time']
            else:
                return None
        else:
            print("No question was asked")
            return None

    def getScores(self): #returns a sorted list of scores.
        if self.newScores != None:
            return self.sortScores(self.newScores)
        else:
            print("No scores have been send")
            return None

    def getYourScore(self): #returns your own score
        if self.newScores != None:
            return self.newScores.get(self.name)
        else:
            print("No scores have been send")
            return None

    def getSolution(self): #returns the correct answer to the last question you answered
        if self.newScores != None:
            return self.solution
        else:
            print("No scores have been send")
            return None

    def getEndMessage(self):
        return self.endMessage

    def end(self): #close the connection
        print("disconnecting from server")
        self.server.close()
        print("done.")























    
