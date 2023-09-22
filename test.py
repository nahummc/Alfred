from alfred import AlfredChat
from datetime import datetime


# this will run a simple 'conversation' with
# chatgpt until the user enters exit or stop

def talking():

    go = True

    while go:

        prompt = input(">>> ")
        if prompt == "exit" or prompt == "stop":
            goodbye = AlfredChat("goodbye").return_completion()
            print("Alfred:: " + goodbye)
            go = False

        # prompt = "Answer this question and give me a fun fact: " + prompt
        completion = AlfredChat(prompt=prompt).return_completion()
        print(completion)
        print("\n\n")

        f = open('test_logs.txt', 'a')
        f.write(completion + "")
        f.write("\n\n")
        f.close()

        


talking()



