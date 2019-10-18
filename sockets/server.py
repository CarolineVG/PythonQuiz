import socket
import pickle
import random
import json

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1236))
s.listen(5)

while True:
    #connect
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")

    #send question
    question = '{"sender": "Host", "id": "0001", "question": "What is the first letter of the alphabet?", "options":{"A":"A","B":"B","C":"C"}}'
    solution = 'A'
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
            print("The answer is: "+answer)

            #check of answer juist is
            if answer == solution:
                print('Correct')
                #clientsocket.sendall(data)
            else:
                print('False!')
                break
                
