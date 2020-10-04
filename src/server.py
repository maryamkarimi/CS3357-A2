# SAVING THINGS LIKE /A/ 

from socket import *
import os

SCRIPT_DIR = os.path.dirname(os.path.realpath('__file__'))

# Adress for the server
TCP_IP = 'localhost'

# Port for the server
TCP_PORT = 8092

BLANK_LINE = '\r\n'


class HTTPStatus:
    # success
    OK = 200, 'OK', 'Request fulfilled, document follows'

    # client error
    NOT_FOUND = 404, 'Not Found', 'Nothing matches the given URI'

    # server errors
    NOT_IMPLEMENTED = 501, 'Method Not Implemented', 'Server does not support this operation'
    HTTP_VERSION_NOT_SUPPORTED = 505, 'Version Not Supported', 'This web server only supports HTTP/1.1.'


class HTTPServer:
    def run(self):

        # Create TCP socket for server
        serverSocket = socket(AF_INET, SOCK_STREAM)

        # Bind the configured sever ip and port
        serverSocket.bind((TCP_IP, TCP_PORT))

        # Start listening for connections
        serverSocket.listen(1)
        print('The server is ready to receive')

        f = open("", 'rb')  # open requested file
        f.close()

        # while True:
        #     connectionSocket, addr = serverSocket.accept()

        #     print('Request recieved from ', addr)

        #     # Read data
        #     request = connectionSocket.recv(1024).decode()

        #     request = request.split(BLANK_LINE)[0]
        #     response = self.handleGet(request.split())

        #     # Send response back to the client
        #     connectionSocket.send(response)
        # connectionSocket.close()

    # GET command  
    def handleGet(self, args):

        content_type = 'text-html'
        response_headers = ''

        if args[0].upper() != 'GET':
            response_line = "HTTP/1.1 %s %s" % (HTTPStatus.NOT_IMPLEMENTED[0], HTTPStatus.NOT_IMPLEMENTED[1])
            response_body = HTTPStatus.NOT_IMPLEMENTED[2].encode()

        elif args[2].upper() != 'HTTP/1.1':
            response_line = "HTTP/1.1 %s %s" % (
            HTTPStatus.HTTP_VERSION_NOT_SUPPORTED[0], HTTPStatus.HTTP_VERSION_NOT_SUPPORTED[1])
            response_body = HTTPStatus.HTTP_VERSION_NOT_SUPPORTED[2].encode()

        else:
            try:
                fileName = args[1]
                f = open(fileName, 'rb')  # open requested file

                response_line = "HTTP/1.1 %s %s" % (HTTPStatus.OK[0], HTTPStatus.OK[1])
                response_body = f.read()

                fileType = args[1].split('.')[1]
                if fileType.upper() == 'JPG' or fileType.upper() == 'JPEG' or fileType.upper() == 'PNG' or fileType.upper() == 'GIF':
                    content_type = fileType

                # send header first
                response_headers = "Content-Length: %s" % (f.tell())

                f.close()

            except Exception:
                response_line = "HTTP/1.1 %s %s" % (HTTPStatus.NOT_FOUND[0], HTTPStatus.NOT_FOUND[1])
                response_body = HTTPStatus.NOT_FOUND[2].encode()

        response_headers = 'Content-type: %s\r\n%s' % (content_type, response_headers)
        response_headers = "%s%s%s%s%s" % (response_line, BLANK_LINE, response_headers, BLANK_LINE, BLANK_LINE)
        response_headers = response_headers.encode()
        return response_headers + response_body


if __name__ == '__main__':
    HTTPServer().run()
