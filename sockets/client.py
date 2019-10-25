import socket
import pickle
import json
import sys

HEADERSIZE = 10 #size of the header of the data we send to the server. In the header we say how long the data is.

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1236))

clientName = input("who are you? ")

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

        #print(message)
            
        if message["type"] == "question":
            print("")
            print(message['question'])
            print('- A: '+message['options']['A'])
            print('- B: '+message['options']['B'])
            if 'C' in message['options']:
                print('- C: '+message['options']['C'])
            if 'D' in message['options']:
                print('- D: '+message['options']['D'])

            # Send answer
            while True:
                print("")
                answer = input("Your answer: ")
                answer = answer.upper()
                if answer == "A" or answer == "B" or answer == "C" or answer == "D":
                    break
                else:
                    print("Please choose between A, B, C or D")
                    continue
            answer = '{"sender":"'+clientName+'", "answer":"'+answer+'"}'
            answer = pickle.dumps(answer)
            answer = bytes(f'{len(answer):<{HEADERSIZE}}', "utf-8") + answer

            s.sendall(answer)
            print("")
            print("Waiting for others to answer...")

        if message["type"] == "scores":

            #print(message["scoreboard"])

            # get users score from dictionary and print it
            yourScore = message["scoreboard"].get(clientName)
            print("")
            print(f"Your current score is {yourScore}")

            #dictionary to list so it can be sorted
            top5 = []
            for record in message["scoreboard"]:
                top5.append([record, message["scoreboard"][record]])
            top5.sort(key=lambda x: x[1], reverse=True)


            #print top 5
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
            print("Prepare yourself for the next question...")
            print("")

        if message["type"] == "end":
            print("this quiz has ended.")
            print(message["message"])
            break

        #reset loop
        new_msg = True
        full_msg = b''
print("exiting program")
sys.exit(0)
    
