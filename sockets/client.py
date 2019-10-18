import socket
import pickle
import json

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1236))


while True:

    full_msg = b''
    new_msg = True
    while True:
        msg = s.recv(8)
        if new_msg:
            #print(f"new message length: {msg[:HEADERSIZE]}")
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        full_msg += msg
        #print(full_msg)
        
        if len(full_msg)-HEADERSIZE == msglen:
            #print("full msg recvd")
            #print(full_msg[HEADERSIZE:])

            d = pickle.loads(full_msg[HEADERSIZE:])
            message = json.loads(d)
            #print(message)
            print(message['question'])

            #print(full_msg)

            # Send answer
            answer = input("Give me a message: ")
            message = pickle.dumps(answer)
            #print(f"answer = {answer}")
            #print(f"message = {message}")

            message = bytes(f'{len(message):<{HEADERSIZE}}', "utf-8") + message
            print('sending '+str(message))
            s.sendall(message)
            

            #reset loop
            new_msg = True
            full_msg = b''

    print(full_msg)
    
