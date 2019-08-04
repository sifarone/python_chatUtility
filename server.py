import socket
import threading
import collections
import helper
import encrypt

# TBD
connections = collections.defaultdict(str)

class myServer():
    host = helper.host
    port = helper.port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self):
        # bind the socket
        myServer.sock.bind((myServer.host, myServer.port))

    def startListening(self, listeners):
        print("Server Running --")
        myServer.sock.listen(listeners)
        while True:
            clientSocket, clientAddr = myServer.sock.accept()
            print ("Connected with : " + str(clientAddr))
            welcomeMsg = encrypt.encrypt("Connection with server established ...")
            clientSocket.send(welcomeMsg, helper.bufferSize)
            clientHdlr = clientHandler(str(clientAddr), "empty Payload", clientSocket)
            clientHdlr.start()

    def setBlockingStatus(self, status):
        myServer.sock.setblocking(status)


class clientHandler(threading.Thread):
    def __init__(self, name, data, sock):
        threading.Thread.__init__(self)
        self.threadName = name
        self.data = data
        self.socket = sock

    def Send(self, socket, text):
        socket.send(encrypt.encrypt(text), helper.bufferSize)

    def Recv(self):
        data = self.socket.recv(helper.bufferSize)
        return encrypt.decrypt(data)

    def run(self):
        global connections
        print("Client Handler : " + self.threadName + "starting ...")
        me = None

        while True:
            data = self.Recv()
            tokens = data.split("/")
            print("-"*50)
            print ("INCOMING : ", data)
            print("-"*50)

            header = tokens[0].strip()
            body = tokens[1].strip()

            print("Message Body : ", body)
            print("Destination : ", header)

            if header == "reg":
                me = body
                connections[me] = self.socket
                print("-"*50)
                print (connections)
                print("-"*50)

            elif header == "all": # Broadcast
                # Broadcast to all the connected clients
                for user in connections:
                    if user == me:
                        pass
                    else:
                        destSocket = connections[user]
                        outMsg = "Broadcast [" + me + " Says ] : " + body
                        self.Send(destSocket, outMsg)

            elif header == "list":
                # Send logged in user list
                msg = str(list(connections.keys()))
                outMsg = "< User List > : " + msg
                destSocket = connections[me]
                self.Send(destSocket, outMsg)

            elif header == "exit":
                break

            elif header == "exec":
                token = body.split(":")
                target = token[0].strip()
                outMsg = "exec/" + token[1]
                destSocket = connections[target]
                self.Send(destSocket, outMsg)

            else: # Routing to other users
                if header not in connections.keys():
                    outMsg = "ERROR: User [" + header + "] does not exist!!"
                    destSocket = connections[me]
                else:
                    destSocket = connections[header]
                    outMsg = "[" + me + " Says ] : " + body

                    self.Send(destSocket, outMsg)

        print ("Closing connection Thread for : ", me)
        del connections[me]
        self.socket.close()

if __name__ == "__main__":
    server = myServer()
    server.startListening(5)