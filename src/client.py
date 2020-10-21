import os
import socket

BLANK_LINE = '\r\n'

BUFFER_SIZE = 1024


class HTTPClient:

    def main(self):
        # Get input from the user
        host_name = input('Input host name (ex. localhost): ')
        try:
            port_number = int(input('Input host name (ex. 8090): '))
        except ValueError:
            print('The entered port is not valid')
            return

        file_name = input('Input file name (ex. index.html): ')

        self.handle_request(host_name, port_number, file_name)

    @staticmethod
    def handle_request(host_name, port_number, file_path):

        # Create Socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Try to connect to server
        try:
            client_socket.connect((host_name, port_number))
            print('Connection Established')
        except ConnectionError:
            print('Error encountered while connecting to server')
            client_socket.close()
            quit()
        except socket.gaierror:
            print('Server name or port number is not valid')
            quit()

        host = "Host: %s:%s" % (host_name, port_number)
        request = "GET %s HTTP/1.1%s%s" % (file_path, BLANK_LINE, host)

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
