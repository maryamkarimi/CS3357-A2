import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 8092

HOST_NAME = '127.0.0.1'

BLANK_LINE = '\r\n'

BUFF_SIZE = 40960000


class HTTPClient:
    def main(self):

        # Create Socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Try to connect to server
        try:
            client_socket.connect((TCP_IP, TCP_PORT))
            print('Connection Established')
        except Exception:
            print('Error encountered while connecting to server')
            client_socket.close()
            quit()

        cmd = input('Input command (ex. GET /index.html HTTP/1.1):')

        host = "Host: %s:" % (HOST_NAME)

        request = "%s%s%s" % (cmd, BLANK_LINE, host)
        client_socket.send(request.encode())

        response = client_socket.recv(BUFF_SIZE)
        headers, sep, body = response.partition(b'\r\n\r\n')

        headers = headers.decode()
        response_code = headers.split(BLANK_LINE)[0].split()[1]

        if response_code == "200":
            file_name = cmd.split()[1]
            f = open(file_name, "wb")
            f.write(body)
            f.close()

        print('From Server: ', headers)
        client_socket.close()
        print('Connection Closed')


if __name__ == '__main__':
    HTTPClient().main()
