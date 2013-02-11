from gittle import GitServer

server = GitServer('/', 'localhost')
server.serve_forever()
