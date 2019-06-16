from http.server import BaseHTTPRequestHandler, HTTPServer
import database
from urllib import parse
import json, os, time

db = database.Message_database()

class Server(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _response_on_request(self, path, query):
        if path == "/send_message":
            db.save_message(query["sender"], query["receiver"], query["message"])
            self.wfile.write(json.dumps({"result": True}).encode("utf-8"))
        elif path == "/get_messages":
            messages = db.get_messages(query["receiver"])
            self.wfile.write(json.dumps(messages).encode("utf-8"))
            #db.delete_messages_of_receiver(query["receiver"])
        elif path == "/got_new_messages":
            if len(db.get_messages(query["receiver"])) > 0:
                self.wfile.write(json.dumps({"result": True}).encode("utf-8"))
            else:
                self.wfile.write(json.dumps({"result": False}).encode("utf-8"))
        elif path == "/delete_messages":
            db.delete_messages_of_receiver(query["receiver"])
            self.wfile.write(json.dumps({"result": True}).encode("utf-8"))

    def do_GET(self):
        self._set_headers()
        query = dict(parse.parse_qsl(parse.urlsplit(self.path).query))
        path = parse.urlsplit(self.path).path
        self._response_on_request(path, query)

    def do_HEAD(self):
        self._set_headers()


    def do_POST(self):
        # Doesn't do anything with posted data

        self._set_headers()
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_str_data = self.rfile.read(content_length)  # <--- Gets the data itself
        post_data = dict(parse.parse_qsl(post_str_data.decode("utf-8")))
        path = parse.urlsplit(self.path).path
        print(post_data, path)
        self._response_on_request(path, post_data)
        #self.wfile.write(json.dumps(db.get_data(self.path[1:], post_data)).encode("utf-8"))



def run(server_class=HTTPServer, handler_class=Server, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()


run()
