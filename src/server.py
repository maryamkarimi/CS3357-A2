import socket

# Address for the server
TCP_IP = 'localhost'

# Port for the server
TCP_PORT = 8090

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
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the configured sever ip and port
        server_socket.bind((TCP_IP, TCP_PORT))

        # Start listening for connections
        server_socket.listen(1)
        print('The server is ready to receive')

        while True:
            connection_socket, addr = server_socket.accept()
            print('Request recieved from ', addr)

            # Read data
            request = connection_socket.recv(1024).decode()

            try:
                request = request.split(BLANK_LINE)[0]
                response = self.handle_get(request.split())

                # Send response back to the client
                connection_socket.send(response)
            except IndexError:
                connection_socket.close()

    # GET command
    @staticmethod
    def handle_get(args):

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
                # if the file name starts with a '/', add a '.' to it so it can be properly handled.
                file_name = args[1]
                if file_name.startswith('/'):
                    file_name = '.' + file_name

                # open requested file
                f = open(file_name, 'rb')

                response_body = f.read()

                file_type = args[1].split('.')[1]
                if file_type.upper() == 'JPG' or file_type.upper() == 'JPEG' or file_type.upper() == 'PNG' or file_type.upper() == 'GIF':
                    content_type = file_type

                # set headers
                response_headers = "Content-Length: %s" % (f.tell())
                response_line = "HTTP/1.1 %s %s" % (HTTPStatus.OK[0], HTTPStatus.OK[1])

                # close the file
                f.close()

            except IOError:
                response_line = "HTTP/1.1 %s %s" % (HTTPStatus.NOT_FOUND[0], HTTPStatus.NOT_FOUND[1])
                response_body = HTTPStatus.NOT_FOUND[2].encode()

        response_headers = 'Content-type: %s\r\n%s' % (content_type, response_headers)
        response_headers = "%s%s%s%s%s" % (response_line, BLANK_LINE, response_headers, BLANK_LINE, BLANK_LINE)
        response_headers = response_headers.encode()
        return response_headers + response_body


if __name__ == '__main__':
    HTTPServer().run()
