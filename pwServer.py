import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import sys
import base64

key = ""

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
            print "self.headers.getheader('Authorization') == NONE"
            self.do_AUTHHEAD()
            self.wfile.write('no auth header received')
            pass
        elif self.headers.getheader('Authorization') == 'Basic '+key:
            print "self.headers.getheader('Authorization') == 'Basic '+key"
            SimpleHTTPRequestHandler.do_GET(self)
            pass
        else:
            print "else:"
            self.do_AUTHHEAD()
            self.wfile.write(self.headers.getheader('Authorization'))
            self.wfile.write('not authenticated')
            pass

def test(HandlerClass = AuthHandler,
         ServerClass = BaseHTTPServer.HTTPServer):
    #clientAddress = ('127.0.0.1',80)
    BaseHTTPServer.test(HandlerClass, ServerClass)
    BaseHTTPServer.clientAddress('127.0.0.1',80)

if __name__ == '__main__':
    if len(sys.argv)<3:
        print "usage pwServer.py [port] [username:password]"
        sys.exit()

    key = base64.b64encode(sys.argv[2])
    test()
