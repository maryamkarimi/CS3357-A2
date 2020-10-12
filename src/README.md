##### A stripped down and simplified web server and web downloader client in Python 

In response to a request, the webserver simply reads the contents of a named file and pushes it back over the same connection.

The webserver only supports the GET request of HTTP/1.1. 

The downloader will open a TCP connection to the server and issue a request like: GET /index.html HTTP/1.1 with an appropriate Host: header.  The server will open this file relative to its current directory, read the contents, and send back the results. The downloader will save the file to disk relative to its own current directory, and close the connection. 
