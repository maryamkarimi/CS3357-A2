from socket import *

TCP_IP = '127.0.0.1'
TCP_PORT = 8092

HOST_NAME = '127.0.0.1'

BLANK_LINE = '\r\n'

BUFF_SIZE = 40960000


class HTTPClient:
    def main(self):

        # Create Socket
        clientSocket = socket(AF_INET, SOCK_STREAM)

        # Try to connect to server
        try:
            clientSocket.connect((TCP_IP, TCP_PORT))
            print('Connection Established')
        except Exception:
            print('Error encountered while connecting to server')
            clientSocket.close()
            quit()

        cmd = input('Input command (ex. GET /index.html HTTP/1.1):')

        host = "Host: %s:" % (HOST_NAME)

        request = "%s%s%s" % (cmd, BLANK_LINE, host)
        clientSocket.send(request.encode())

        response = clientSocket.recv(BUFF_SIZE)
        headers, sep, body = response.partition(b'\r\n\r\n')

        headers = headers.decode()
        responseCode = headers.split(BLANK_LINE)[0].split()[1]

        if responseCode == "200":
            fileName = cmd.split()[1]
            f = open(fileName, "wb")
            f.write(body)
            f.close()

        print('From Server: ', headers)
        clientSocket.close()
        print('Connection Closed')


if __name__ == '__main__':
    HTTPClient().main()
