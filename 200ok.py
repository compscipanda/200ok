import socket
from urllib.parse import urlparse

"""
The term CRLF refers to Carriage Return (ASCII 13, \r)
Line Feed (ASCII 10, \n).
They're used to note the termination of a line,
however, dealt with
differently in today's popular Operating Systems.
"""
CRLF = '\r\n'
SP = ' '
CR = '\r'
PATH = '/'
PORT = 443

urls = [
    "https://geeksforgeeks.com/"
]

payloads = [
    "GET / HTTP/1.1" + CRLF + CRLF, # send http request
    "GET / HTTP/1.1" + CRLF + "Host: {}" + CRLF + "Host: localhost" + CRLF + CRLF, # send host = localhost
    "GET / HTTP/1.1" + CRLF + "host: {}" + CRLF + CRLF, # lowercase host header,
    "GET / HTTP/1.1" + CRLF + "Host:{}" + CRLF + CRLF, # removed space in host header
]


def parse_header(header):
    header_fields = header.split(CR)
    # The first line of a Response message is the 
    # Status-Line, consisting of the protocol version 
    # followed by a numeric status code and its 
    # associated textual phrase, with each element 
    # separated by SP characters.

    # Get the numeric status code from the status
    # line.
    code = header_fields.pop(0).split(' ')[1]
    return code


def send_request(payload, host, port=PORT):
    """
    Send a request.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_ip = socket.gethostbyname(host)
    print(host_ip)
    # Connect to the server.
    sock.connect((host_ip, port))
    # Send the request.
    sock.send(payload.encode('utf-8'))

    # Get the response.
    chunks = []
    while True:
        chunk = sock.recv(2048)
        if chunk:
            chunks.append(chunk.decode('utf-8'))
        else:
            break

    response = ''.join(chunks)

    # HTTP headers will be separated from the body by an empty line
    header, _, _ = response.partition(CRLF + CRLF)
    print(header)
    code = parse_header(header)
    return code


def main():
    for url in urls:
        url = urlparse(url)
        for payload in payloads:
            payload = payload.format(url.netloc)
            code  = send_request(payload, url.netloc)
            print(code)


if __name__ == "__main__":
    main()