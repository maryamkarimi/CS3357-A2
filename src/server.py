import socket
from enum import Enum

# Address for the server
TCP_IP = '127.0.0.1'

# Port for the server
TCP_PORT = 8090

BLANK_LINE = '\r\n'

BUFFER_SIZE = 1024


class HTTPStatus(Enum):
    # success
    OK = (200, 'OK', 'Request fulfilled, document follows')

    # client error
    NOT_FOUND = (404, 'Not Found', 'Nothing matches the given URI')

    # server errors
    NOT_IMPLEMENTED = (501, 'Method Not Implemented', 'Server does not support this operation')
    HTTP_VERSION_NOT_SUPPORTED = (505, 'Version Not Supported', 'This web server only supports HTTP/1.1.')

    def __init__(self, status_code, status_description, status_message):
        self.status_code = status_code
        self.status_description = status_description
        self.status_message = status_message


class HTTPServer:
    def run(self):

        # Create TCP socket for server
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the configured sever ip and port
        server_socket.bind((TCP_IP, TCP_PORT))

        # Start listening for connections
        server_socket.listen(1)
        print('The server is ready to receive on port', TCP_PORT)

        while True:
            connection_socket, addr = server_socket.accept()
            print('Request received from ', addr)

            # Read data
            request = connection_socket.recv(BUFFER_SIZE).decode()

            try:
                request = request.split(BLANK_LINE)[0]
                response = self.handle_get(request.split())

                # Send response back to the client
                connection_socket.send(response)

                # close the connection
                connection_socket.close()
            except ValueError:
                connection_socket.close()

    # GET command
    def handle_get(self, args):

        method, file_name, http_version = args
        content_type = 'text-html'
        response_headers = ''
        response_body = ''

        if method.upper() != 'GET':
            status = HTTPStatus.NOT_IMPLEMENTED

        elif http_version.upper() != 'HTTP/1.1':
            status = HTTPStatus.HTTP_VERSION_NOT_SUPPORTED

        else:
            try:
                # if the file name starts with a '/', add a '.' to it so it can be properly handled.
                if file_name.startswith('/'):
                    file_name = '.' + file_name

                # open requested file
                f = open(file_name, 'rb')

                response_body = f.read()

                file_type = file_name.split('.')[1].upper()
                if file_type == 'JPG' or file_type == 'JPEG' or file_type == 'PNG' or file_type == 'GIF':
                    content_type = file_type

                # set headers and status
                file_size = f.tell()
                response_headers = 'Content-Length: %s' % file_size
                status = HTTPStatus.OK

                # close the file
                f.close()

            except IOError:
                status = HTTPStatus.NOT_FOUND

        response_line = self.get_response_line(status.status_code, status.status_description)

        if status != HTTPStatus.OK:
            response_body = status.status_message.encode()

        response_headers = 'Content-type: %s%s%s' % (content_type, BLANK_LINE, response_headers)
        response_headers = '%s%s%s%s%s' % (response_line, BLANK_LINE, response_headers, BLANK_LINE, BLANK_LINE)
        return response_headers.encode() + response_body

    @staticmethod
    def get_response_line(response_code, response_description):
        return 'HTTP/1.1 %s %s' % (response_code, response_description)


if __name__ == '__main__':
    HTTPServer().run()
