from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from todo import DatabaseManager

db_manager = DatabaseManager("todo.db")

class TodosHttpRequestHandler(BaseHTTPRequestHandler):
    def set_headers(self, status=200, data=None):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        if data:
            self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        if self.path == '/todos':
            todos = db_manager.get_all()
            todos_list = [dict(id=row[0], task=row[1], done=row[2]) for row in todos]
            self.set_headers(200, todos_list)
        else:
            self.set_headers(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/todos':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            task = data.get('task')
            done = data.get('done', False)
            db_manager.create(task, done)
            self.set_headers(201)
            self.end_headers()
        else:
            self.set_headers(404)
            self.end_headers()

    def do_PUT(self, ):
        if self.path.startswith('/todos/'):

            pk = int(self.path.split('/')[-1])
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode()
            data = json.loads(post_data)
            task = data.get('task')
            done = data.get('done')
            db_manager.update(pk, task, done)
            self.set_headers(200)
            self.end_headers()
        else:
            self.set_headers(404)
            self.end_headers()

    def do_DELETE(self):
        if self.path.startswith('/todos/'):
            pk = int(self.path.split('/')[-1])
            db_manager.delete(pk)
            self.set_headers(204)
            self.end_headers()
        else:
            self.set_headers(404)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=TodosHttpRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == "__main__":
    run()
