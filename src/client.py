import os
import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 8090

HOST_NAME = '127.0.0.1'

BLANK_LINE = '\r\n'

BUFFER_SIZE = 1024


class HTTPClient:

    def main(self):
        # Get command from the user
        cmd = input('Input command (ex. GET /index.html HTTP/1.1):')
        # If the command format is incorrect, i.e. "GET", "GET /index.html"
        if len(cmd.split(' ')) != 3:
            print('Please enter valid command (ex. GET /index.html HTTP/1.1)')
        else:
            self.handle_request(cmd)

    @staticmethod
    def handle_request(cmd):

        # Create Socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Try to connect to server
        try:
            client_socket.connect((TCP_IP, TCP_PORT))
            print('Connection Established')
        except ConnectionError:
            print('Error encountered while connecting to server')
            client_socket.close()
            quit()

        host = "Host: %s:" % HOST_NAME
        request = "%s%s%s" % (cmd, BLANK_LINE, host)

        # Send request to the server
        client_socket.send(request.encode())

        # Receive response from the server
        response = b''
        while True:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break
            response += data

        headers, sep, body = response.partition(b'\r\n\r\n')
        headers = headers.decode()
        response_code = headers.split(BLANK_LINE)[0].split()[1]

        print('---------------------------------------------------')
        if response_code == "200":
            # Get the file name without the full path and write to it
            file_path = cmd.split()[1]
            file_name = os.path.basename(file_path)
            f = open(file_name, "wb")
            f.write(body)
            f.close()
            print('From Server: ', headers)
            print('---------------------------------------------------')
            print('File downloaded successfully')
        else:
            print('From Server: ', response.decode())
            print('---------------------------------------------------')

        client_socket.close()
        print('Connection Closed')


if __name__ == '__main__':
    HTTPClient().main()
