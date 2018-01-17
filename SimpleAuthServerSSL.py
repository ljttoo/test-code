import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import sys
import os
import base64
import ssl
import SocketServer

key = ""
#CERTFILE_PATH = "/root/server.pem"

CERTFILE_PATH = "server.crt"
KEYFILE_PATH = "server.key"

class AuthHandler(SimpleHTTPRequestHandler):
    ''' Main class to present webpages and authentication. '''
    print "AuthHandler"
    def do_HEAD(self):
        print "do_HEAD"
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_AUTHHEAD(self):
        print "do_AUTHHEAD"
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        global key
        print "do_GET"
        ''' Present frontpage with user authentication. '''
        if self.headers.getheader('Authorization') == None:
            print "self.headers.getheader('Authorization') == None"
            self.do_AUTHHEAD()
            self.wfile.write('no auth header received')
            pass
        elif self.headers.getheader('Authorization') == 'Basic '+key:
            print "self.headers.getheader('Authorization') == 'Basic '+key"
            SimpleHTTPRequestHandler.do_GET(self)
            pass
        else:
            print "else"
            self.do_AUTHHEAD()
            self.wfile.write(self.headers.getheader('Authorization'))
            self.wfile.write('not authenticated')
            pass

def serve_https(https_port=80, HandlerClass = AuthHandler,
         ServerClass = BaseHTTPServer.HTTPServer):
    httpd = SocketServer.TCPServer(("127.0.0.1", https_port), HandlerClass)
    httpd.socket = ssl.wrap_socket (httpd.socket, keyfile=KEYFILE_PATH, certfile=CERTFILE_PATH, server_side=True)

    sa = httpd.socket.getsockname()
    print "Serving HTTP on", sa[0], "port", sa[1], "..."
    httpd.serve_forever()

if __name__ == '__main__':
    HOST,PORT = "localhost", 5000
    https_port = 5000
    print len(sys.argv)
    if len(sys.argv)<3:
        print "usage SimpleAuthServer.py [port] [username:password]"
        sys.exit()

    https_port = int(sys.argv[1])
    key = base64.b64encode(sys.argv[2])

    if len(sys.argv) == 4:
        change_dir = sys.argv[3]
        print "Changing dir to {cd}".format(cd=change_dir)
        os.chdir(change_dir)

    serve_https(https_port=https_port)

