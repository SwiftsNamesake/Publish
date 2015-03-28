#
# main.py
# ...
#
# Jonatan H Sundqvist
# March 28 2015
#

# TODO | - Logging (database, plain text)
#        - Security, privileges, encryption, https
#        - API (restful)
#          -- Searching
#          -- Queries (by date, by title, by id, etc.)
#          -- Posting
#          -- Listing entries
#        - Threading (?)

# SPEC | -
#        -



# from os import curdir, sep
# from os.path import splitext, join, exists
# from urllib.parse import urlparse

import webutils #
import database #

from SwiftUtils.SwiftUtils import ordinal # TEST

import string, cgi, time

from os import path

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote, urlparse, parse_qs, ParseResult



class Publisher(BaseHTTPRequestHandler):

	'''
	Docstring goes here

	'''


	def do_GET(self):

		'''
		Handles GET requests

		'''
		

		#
		# TODO: Use platform-independent functions to construct the full path (...)
		print('Processing GET request ({path})...'.format(path=self.path))
		url = ParseResult(*(unquote(part) for part in urlparse(self.path))) # Unpack url components and decode HTML escapes (%xx)
		
		if path.splitext(url.path)[-1] not in webutils.contentTypes:
			# TODO: Response code
			print('Empty or invalid URL')
			return

		ctype    = webutils.contentTypeFromPath(self.path)	# Content type
		category = ctype.split('/')[0] # Content type category (eg. image, text, etc.)
		query = parse_qs(url.query, keep_blank_values=True, strict_parsing=False, encoding='utf-8', errors='replace') # 
		echo = '</br>'.join('<strong>{0}</strong>: {1}'.format(key, val) for key, val in query.items()) 		 	 # Inefficient

		# TODO: Find a less error-prone procedure for determining the file type

		if category == 'dynamic':
			# Dynamic content
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()

			day = time.localtime()[7]
			year = time.localtime()[0]

			webutils.sendUnicode(self.wfile, '\n'.join((
				'<link rel="shortcut icon" type="image/png" href="C:/Users/Jonatan/Desktop/Web%20dev/Ajax/Ajax.png">',
				'<p>Today is the <strong>{day}</strong><sup>{ord}</sup> day in the year <strong style="color:red;font-family:Courier">{year}</strong>.</p>',
				'<p>The items you requested:</br>{echo}</p>',
				'<p>Head over to the <a href="http://hem.bredband.net/swiftsnamesake/">main page</a></p>',
				'<img src="http://www.paul-cezanne.org/Still-Life-with-Basket-of-Apples.jpg"><img/>')).format(day=day, ord=ordinal(day), year=year, echo=echo)
			)

		elif not path.exists(url.path):
			# Invalid path
			print("404:", url.path)
			self.send_error(404, 'File Not Found: %s' % url.path)

		elif category == 'text':
			# The Holy Trinity (or plaintext)
			with open(url.path, 'rb') as f:
				self.send_response(200)
				self.send_header('Content-type', ctype)
				self.end_headers()
				self.sendUnicode(f)

		elif category == 'image':
			# Images
			with open(url.path, 'rb') as f:
				self.send_response(200)
				self.send_header('Content-type', ctype)
				self.end_headers()
				self.wfile.write(f.read())

		elif '.' not in self.path:
			# Custom queries
			self.send_error(501, 'Unable to handle your request at this moment.')


	def do_POST(self):

		''' 
		Handles POST requests

 		'''
		
		print('Handling POST request')
		
		try:
			ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			
			if ctype == 'multipart/form-data':
				query = cgi.parse_multipart(self.rfile, pdict)
			
			self.send_response(301)

			self.end_headers()
			upfilecontent = query.get('upfile')
			
			print ('filecontent', upfilecontent[0])
			
			self.wfile.write('<html>POST OK.<br><br></html>')
			self.wfile.write(upfilecontent[0])

		except Exception as e:
			print('The all-inclusive except')



def createRequestServer():

	'''
	Docstring goes here
	
	'''

	pass



def main():
	
	'''
	Docstring goes here

	'''

	try:
		server = HTTPServer(('', 80), Publisher)
		print('Started httpserver at port {port}...'.format(port=80))
		server.serve_forever()
	except KeyboardInterrupt:
		server.socket.close()



if __name__ == '__main__':
	main()