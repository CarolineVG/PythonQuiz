import socket
import pickle
import random
import json
import threading
import time
import sys
import netifaces as ni

'''
for i in ni.interfaces():
    print(str(i))
'''
SERVER_IP = input("Enter your local IP: ")
if SERVER_IP == "":
    SERVER_IP = socket.gethostname() #localhost

HEADERSIZE = 10 #size of the header of the data we send to the client. In the header we say how long the data is.
clients = set() #a set of all clients that are connected
answers = 0 #a counter that keeps track of how many clients have answered already
scores = {} #the scoreboard

questions = [ #list of (for now hard-coded) questions that the clients will answer
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
    ]

currentQuestion = 0 # position of the next question to be send

def sendToAll(json):
    json = pickle.dumps(json)
    json = bytes(f'{len(json):<{HEADERSIZE}}', "utf-8") + json
    for c in clients:
        c.sendall(json)
        #print(f"sending to {c}")

def sortScores(scores):
    top5 = []
    for record in scores:
        top5.append([record, scores[record]])
    top5.sort(key=lambda x: x[1], reverse=True)
    return top5

def sendQuestion(clientsocket, question):

    solution = question['solution']
    if 'time' in question:
        question = '{"type":"question", "sender": "Host", "id":"'+question['id']+'", "question": "'+question['question']+'", "options":'+json.dumps(question['options'])+',"time":'+json.dumps(question['time'])+'}'
    else:
        question = '{"type":"question", "sender": "Host", "id":"'+question['id']+'", "question": "'+question['question']+'", "options":'+json.dumps(question['options'])+'}'
    #print(question)
    #print(solution)
    
    #send question
    msg = pickle.dumps(question)
    
    msg = bytes(f'{len(msg):<{HEADERSIZE}}', "utf-8") + msg

    #print(msg)
    
    clientsocket.send(msg)

    #await response
    full_answer = b''
    new_answer = True
    while True:
        response = clientsocket.recv(8)
        if new_answer:
            answerlen = int(response[:HEADERSIZE])
            new_answer = False

        full_answer += response
        #print(full_answer)
        if len(full_answer)-HEADERSIZE == answerlen:
            answer = pickle.loads(full_answer[HEADERSIZE:])
            answer = json.loads(answer)
            #print("The answer is: "+answer["answer"])
            
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
                global questions
                global currentQuestion
                if currentQuestion == len(questions)-1:
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

def handleQuiz(clientsocket, questions):
    position = currentQuestion
    while True:
        if position == currentQuestion:
            time.sleep(1)
            if position != len(questions):
                sendQuestion(clientsocket, questions[position])
            else:
                break
            position = position + 1
    global end
    end = True
    return

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((SERVER_IP, 5000))
    s.listen(5)

    while True:
        clientsocket, address = s.accept()
        if access == False:
            #send back message to client so the client will close connection (I can't figure out how to do it from here)
            msg = '{"type":"connection refused"}'
            msg = pickle.dumps(msg)
            msg = bytes(f'{len(msg):<{HEADERSIZE}}', "utf-8") + msg
            clientsocket.send(msg)
        else:
            clients.add(clientsocket)
            print(f"{len(clients)} players have connected.")
            


access = True
a = threading.Thread(target=connect)
a.start()
when = input("Listening for players...\nPress enter when enough players have joined.\n\n") #say when
if when != None:
    access = False
    if len(clients)>=1:
        print("The quiz has started!")
        for c in clients:
            x = threading.Thread(target=handleQuiz, args=(c, questions))
            x.start()
    else:
        print("No players were found.")
        sys.exit(0)

end = False
while True:
    if end:
        print("The quiz is over")
        print("")
        print(f"The winner is {sortScores(scores)[0][0]}!")
        if len(scores) >= 2:
            print(f"{sortScores(scores)[1][0]} is second.")
        if len(scores) >= 3:
            print(f"{sortScores(scores)[2][0]} is third.")
        break
