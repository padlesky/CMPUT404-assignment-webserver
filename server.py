import SocketServer
import os
# coding: utf-8

# Copyright 2015 Pranjali Pokharel, Aaron Padlesky
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# Also contains contributions from Abram Hindle and Eddie Antonio Santos
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        self.dataList = self.data.split()
        if self.dataList[0] == "GET":
            self.get()
        else:
            self.request.sendall("OK")

    def get(self):
        #Used to handle a get request/ Respond to a GET request
        #checks to see if 404 error is thrown
        try:
            sendReply = False

            if self.dataList[1]=="/":
                self.dataList[1] = "/index.html"

            if self.dataList[1] == "/deep":
                self.request.send("HTTP/1.1 301 \r\n")
                self.request.send("Location: deep/ \r\n\r\n")
                return

            if self.dataList[1] == "/deep/":
                self.dataList[1] = "/deep/index.html"

            if self.dataList[1].endswith(".html"):
                mimeType="text/html"
                sendReply = True
            if self.dataList[1].endswith(".css"):
                mimeType="text/css"
                sendReply = True
            if os.path.exists(os.getcwd()+"www"+self.dataList[1]):
                sendReply = False

            if sendReply:
                staticFile = open("www"+ self.dataList[1])
        
                self.request.send("HTTP/1.1 200\r\n")
                self.request.send("Content-Type: %s\r\n\n" %mimeType)
                self.request.send(staticFile.read())
                staticFile.close()
            else:
                self.request.send("HTTP/1.1 404 Not Found\r\n")
                self.request.send("Content-Type: text/html\r\n\n")
                self.request.send("<html><head>Error</head><body>404, File Not Found %s</body></html>" %self.dataList[1])

        except:
            self.request.send("HTTP/1.1 404 Not Found\r\n\n")

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print ' was pushed, server will be shut down'
        server.socket.close()


