import socket
import pickle
import random
import json
import threading

HEADERSIZE = 10

scores = []

def sendQuestion(clientsocket, address, question, solution):
    print("sending question...")
    
    #send question
    msg = pickle.dumps(question)
    
    msg = bytes(f'{len(msg):<{HEADERSIZE}}', "utf-8") + msg

    #print(f"bytes msg = {msg}")
    
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
            print("The answer is: "+answer["answer"])

            #check if the answer was correct
            if answer["answer"] == solution:
                #check if client is already in the scores
                if answer["sender"] in scores:
                    print("tijdelijk")
                    #scores[answer["sender"]] = scores.get(answer["sender"]) + 1
                else:
                    scores.append([answer["sender"], 1])
            top5 = '{"type":"top5", "scoreboard":"'+str(scores)+'"}'
            top5 = pickle.dumps(top5)
            top5 = bytes(f'{len(top5):<{HEADERSIZE}}', "utf-8") + top5
            clientsocket.sendall(top5)

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 1236))
    s.listen(5)
    while True:
        #connect
        clientsocket, address = s.accept()
        print(f"Connection from {address} has been established!")

        x = threading.Thread(target=sendQuestion, args=(clientsocket, address, '{"type":"question", "sender": "Host", "id": "0001", "question": "What is the first letter of the alphabet?", "options":{"A":"A","B":"B","C":"C"}}', 'A'))
        x.start()


connect()
