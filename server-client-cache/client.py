import socket


port = 8001
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('localhost', port))

filename = '/index.html'
s.sendall(filename.encode())

content = s.recv(1024).decode()
check = content
while check:
	check = s.recv(1024)
	content+=check.decode()

print('File fetched from server'+'\n'+'It\'s contents are \n')
print(content)

s.close()
