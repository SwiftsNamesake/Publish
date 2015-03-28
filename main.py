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



connection = database.createDatabase('site.db') # TODO: Move this
database.createDummyEntries(connection)



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
		
		print(url.path)
		if not (path.splitext(url.path)[-1] in webutils.contentTypes or url.path == '/entry'):
			# TODO: Better url validation
			# TODO: Response code
			print('Empty or invalid URL')
			return

		ctype    = webutils.contentTypeFromPath(self.path)	# Content type
		category = ctype.split('/')[0] # Content type category (eg. image, text, etc.)
		query = parse_qs(url.query, keep_blank_values=True, strict_parsing=False, encoding='utf-8', errors='replace') # 

		# TODO: Find a less error-prone procedure for determining the file type

		if url.path == '/entry':
			# Request for a blog entry
			# TODO: Not sure if this (entry path) is the best approach
			entry = database.fetchEntry(connection, ID=int(query['id'][0]))
			# print(entry[4])
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			webutils.sendUnicode(self.wfile, '<DOCTYPE html>\n<html>{contents}</br><strong>你好世界</strong></html>'.format(contents=entry[4]))

		elif category == 'dynamic':
			# Dynamic content
			pass

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
				webutils.sendUnicode(self.wfile, f)

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
		
		# TODO: Figure out what all of this means...

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