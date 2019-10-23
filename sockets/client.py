import socket
import pickle
import json

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1236))

clientName = input("who are you? ")
while True:

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

            print(message)
            
            if message["type"] == "question":
                print(message['question'])
                print('- A: '+message['options']['A'])
                print('- B: '+message['options']['B'])
                if 'C' in message['options']:
                    print('- C: '+message['options']['C'])
                if 'D' in message['options']:
                    print('- D: '+message['options']['D'])

                # Send answer
                while True:
                    answer = input("Choose your option: ")
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
                print("Waiting for others to answer...")

            if message["type"] == "top5":
                print("We got the scores!")

            #reset loop
            new_msg = True
            full_msg = b''

    print(full_msg)
    
