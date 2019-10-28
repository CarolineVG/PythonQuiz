import socket
import pickle
import json
import sys
import time
import threading

HEADERSIZE = 10 #size of the header of the data we send to the server. In the header we say how long the data is.

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1236))

clientName = input("who are you? ")
print("Waiting for the quiz host to send the first question.")

def sortScores(scores):
    top5 = []
    for record in scores:
        top5.append([record, scores[record]])
    top5.sort(key=lambda x: x[1], reverse=True)
    return top5

timeOut = False

def timer(seconds):
    time.sleep(seconds)
    global timeOut
    timeOut = True

full_msg = b''
new_msg = True
while True:
    msg = s.recv(8)
    if new_msg:
        msglen = int(msg[:HEADERSIZE])
        new_msg = False

    full_msg += msg
    #print(full_msg)
        
    if len(full_msg)-HEADERSIZE == msglen:

        d = pickle.loads(full_msg[HEADERSIZE:])
        message = json.loads(d)

        if message["type"] == "connection refused":
            print("")
            print("You were too late. The quiz has already started without you.")
            break
            
        if message["type"] == "question":
            print("")
            print(message['question'])
            print('- A: '+message['options']['A'])
            print('- B: '+message['options']['B'])
            if 'C' in message['options']:
                print('- C: '+message['options']['C'])
            if 'D' in message['options']:
                print('- D: '+message['options']['D'])

            if 'time' in message:
                print(f"you have {message['time']} seconds!")
                timeOut = False
                x = threading.Thread(target=timer, args=([message['time']]))
                x.start()

            # ask answer and validate input
            while True:
                print("")
                answer = input("Your answer: ")
                answer = answer.upper()
                if answer == "A" or answer == "B" or answer == "C" or answer == "D":
                    break
                else:
                    print("Please choose between A, B, C or D")
                    continue
            #send answer
            if timeOut:
                print("You didn't answer in time!")
                answer = '{"sender":"'+clientName+'", "answer":"out of time"}'
            else:
                answer = '{"sender":"'+clientName+'", "answer":"'+answer+'"}'
            answer = pickle.dumps(answer)
            answer = bytes(f'{len(answer):<{HEADERSIZE}}', "utf-8") + answer

            s.sendall(answer)
            print("")
            print("Waiting for others to answer...")

        if message["type"] == "scores":

            # get users score from dictionary and print it
            yourScore = message["scoreboard"].get(clientName)
            print("")
            print(f"Your current score is {yourScore}")

            #dictionary to list so it can be sorted
            top5 = sortScores(message["scoreboard"])

            #print top 5
            print("")
            if 'endMessage' not in message:
                print("Current scoreboard:")
            else:
                print("Final scores:")
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
            
            if 'endMessage' not in message:
                print("Prepare yourself for the next question...")
                print("")
            else:
                print("The quiz has ended.")
                print("")
                if top5[0][0] == clientName:
                    print("You won!")
                if (len(top5) >= 2) and (top5[1][0] == clientName):
                    print("You came in second!")
                if (len(top5) >= 3) and (top5[2][0] == clientName):
                    print("You came in third!")
                print("")
                print(message["endMessage"])
                break
        #reset loop
        new_msg = True
        full_msg = b''
print("exiting program")
sys.exit(0)
    
