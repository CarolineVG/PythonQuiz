import socket
import pickle
import random
import json
import threading
import time

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
            'solution':'C'
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
            'solution':'C'
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

def sendQuestion(clientsocket, address, question):

    solution = question['solution']
    question = '{"type":"question", "sender": "Host", "id":"'+question['id']+'", "question": "'+question['question']+'", "options":'+json.dumps(question['options'])+'}'

    #print(question)
    #print(solution)
    
    #send question
    msg = pickle.dumps(question)
    
    msg = bytes(f'{len(msg):<{HEADERSIZE}}', "utf-8") + msg

    #print(msg)
    
    clientsocket.send(msg)
    print(f"send a new question to {address}")

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
                scoreboard = '{"type":"scores", "scoreboard":'+json.dumps(scores)+'}'
                sendToAll(scoreboard)
                print("scores have been send")
                answers = 0
                global currentQuestion
                currentQuestion = currentQuestion + 1
            return

def handleQuiz(clientsocket, address, questions):
    position = currentQuestion
    sendQuestion(clientsocket, address, questions[0])
    while True:
        if position < currentQuestion:
            position = position + 1
            time.sleep(1)
            if position != len(questions):
                sendQuestion(clientsocket, address, questions[position])
            else:
                break
    endMsg = pickle.dumps('{"type":"end", "message":"Thank you for playing!"}') #this message could be a custom variable
    endMsg = bytes(f'{len(endMsg):<{HEADERSIZE}}', "utf-8") + endMsg
    clientsocket.send(endMsg)
    return

def startQuiz():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 1236))
    s.listen(5)
    while True:
        print("listening for new players")
        #connect
        clientsocket, address = s.accept()
        print(f"Connection from {address} has been established!")
        
        global clients
        clients.add(clientsocket)

        x = threading.Thread(target=handleQuiz, args=(clientsocket, address, questions))
        x.start()

startQuiz()
