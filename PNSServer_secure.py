#Copyright , mitel.com 

import socket
import random
import time
import string,cgi
import os 
from SocketServer import BaseServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from OpenSSL import SSL
import json
import ConfigParser
import httplib

Config = ConfigParser.ConfigParser()

PNSNoti = "/pushnotification/v1.0/message"
def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

class SecureHTTPServer(HTTPServer):
    def __init__(self, server_address, HandlerClass):
        BaseServer.__init__(self, server_address, HandlerClass)
        ctx = SSL.Context(SSL.SSLv23_METHOD)
        #server.pem's location (containing the server private key and the server certificate).
        fpem = 'server.pem'
        ctx.use_privatekey_file (fpem)
        ctx.use_certificate_file(fpem)
        self.socket = SSL.Connection(ctx, socket.socket(self.address_family,self.socket_type))
        self.server_bind()
        self.server_activate()
class MyHandler(SimpleHTTPRequestHandler):
    def setup(self):
        self.connection = self.request
        self.rfile = socket._fileobject(self.request, "rb", self.rbufsize)
        self.wfile = socket._fileobject(self.request, "wb", self.wbufsize)
        
    
    def do_POST(self):
    	try:
	    	print "self.path"
	    	path = self.path    
    		if PNSNoti == path:
    			AppCount = random.randint(1,100)
    			print AppCount      # using this random value to send error responce randomly 
    			print PNSNoti + 'is in' + path
    			if AppCount==5:
    				self.send_response(400)
    			elif AppCount==7:
    				self.send_response(500)
    			elif AppCount==9:
    				self.send_response(503)
    			else:
    				self.send_response(204)
		

    	except IOError:
    		self.send_error(404,'File Not Found: %s' % self.path)
def main():
    try:
        server = SecureHTTPServer(('', 446), MyHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()


