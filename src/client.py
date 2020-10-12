import os
import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 8090

HOST_NAME = '127.0.0.1'

BLANK_LINE = '\r\n'

BUFF_SIZE = 40960000


class HTTPClient:
    @staticmethod
    def main():

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

        cmd = input('Input command (ex. GET /index.html HTTP/1.1):')

        host = "Host: %s:" % HOST_NAME

        request = "%s%s%s" % (cmd, BLANK_LINE, host)
        client_socket.send(request.encode())

        # Receive response from the server
        response = client_socket.recv(BUFF_SIZE)

        try:
            headers, sep, body = response.partition(b'\r\n\r\n')
            headers = headers.decode()
            response_code = headers.split(BLANK_LINE)[0].split()[1]

            if response_code == "200":
                # Get the file name without the full path and write to it
                file_name = os.path.basename(cmd.split()[1])
                f = open(file_name, "wb")
                f.write(body)
                f.close()

            print('From Server: ', headers)

        except IndexError:
            print('Please enter valid command (ex. GET /index.html HTTP/1.1)')

        client_socket.close()
        print('Connection Closed')


if __name__ == '__main__':
    HTTPClient().main()
