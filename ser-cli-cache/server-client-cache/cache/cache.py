
import socket

def fetch_file(filename):
    file_from_cache = fetch_from_cache(filename)

    if file_from_cache:
        print('Fetched successfully from cache.')
        return file_from_cache
    else:
        print('Not in cache. Fetching from server.')
        file_from_server = fetch_from_server(filename)

        if file_from_server:
            save_in_cache(filename, file_from_server)
            return file_from_server
        else:
            return None


def fetch_from_cache(filename):
    try:
        fin = open('cache' + filename)
        content = fin.read()
        fin.close()
        return content
    except IOError:
        return None


def fetch_from_server(filename):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect(('localhost', 8000))

    s.sendall(filename.encode())

    content = s.recv(1024)
    check = content
    while check:
        check = s.recv(1024)
        content += check

    s.close()
    if not content.decode() == 'File Not Found':
        return content.decode()
    else:
        None


def save_in_cache(filename, content):
    print('Saving a copy of {} in the cache'.format(filename))
    cached_file = open('cache' + filename, 'w')
    cached_file.write(content)
    cached_file.close()


SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8001

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((SERVER_HOST, SERVER_PORT))

server_socket.listen(1)

print('Cache proxy is listening on port %s ...' % SERVER_PORT)

while True:
    client_connection, client_address = server_socket.accept()
    request = client_connection.recv(1024).decode()
    filename = request
    content = fetch_file(filename)

    if content:
        response = content
    else:
        response = 'File Not Found'
    client_connection.sendall(response.encode())
    client_connection.close()

server_socket.close()