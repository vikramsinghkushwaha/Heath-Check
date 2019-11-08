
import socket

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((SERVER_HOST, SERVER_PORT))

server_socket.listen(1)

print('Listening on port %s ... ' % SERVER_PORT)

while True:
    client_connection, client_address = server_socket.accept()

    request = client_connection.recv(1024).decode()

    filename = request

    try:
        fin = open('public' + filename)
        content = fin.read(1024)
        while content:
            client_connection.send(content.encode())
            content = fin.read(1024)
        fin.close()
        client_connection.shutdown(socket.SHUT_WR)

    except IOError:
        response = 'File Not Found'
        client_connection.sendall(response.encode())

    client_connection.close()

server_socket.close()


