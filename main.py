#
# main.py
# ...
#
# Jonatan H Sundqvist
# March 28 2015
#

# TODO | - Logging (database, plain text)
#        - Security, privileges, encryption, https, hashes, salts, etc.
#        - API (restful)
#          -- Searching
#          -- Queries (by date, by title, by id, etc.)
#          -- Posting
#          -- Listing entries
#          -- JSON
#
#        - Threading (?)
#        - Custom error pages
#        - Robustnes
#          -- Unit tests, dry runs
#          -- Static checks (?)
#
#        - Read up on the BaseHTTPRequestHandler class and networking in general
#        - Users (table in database)
#        - HTML utilities
#        - Prevent server from stalling because of the console (eg. when selecting text)


# SPEC | -
#        -



# from os import curdir, sep
# from os.path import splitext, join, exists
# from urllib.parse import urlparse

import webutils #
import database #

from SwiftUtils.SwiftUtils import ordinal # TEST

import json
# import string, cgi, time

from os import path

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote, urlparse, parse_qs, ParseResult



# TODO: Close file properly
# TODO: Move initialisation code into separate function
pageTemplate  = open('pageTemplate.html',  'r', encoding='UTF-8').read()
entryTemplate = open('entrytemplate.html', 'r', encoding='UTF-8').read()

connection = database.createDatabase('site.db') # TODO: Move this
database.createDummyEntries(connection, overwrite=True)

webutils.consoleDivider(header='Welcome', length=85)

port = 80
root = 'C:/Users/Jonatan/Desktop/Python/projects/Publish/' # TODO: Prevent upwards relative paths



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
		webutils.log('Processing GET request ({path})...'.format(path=self.path))
		self.dispatch('GET', self.path)

		webutils.consoleDivider(length=85) # TODO: Fancy console output (?)


	def do_POST(self):

		''' 
		Handles POST requests

 		'''
		
		# TODO: Figure out what all of this means...

		webutils.log('Processing POST request ({path})...'.format(path=self.path))
		self.dispatch('POST', self.path)

		if False:
			try:
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				
				if ctype == 'multipart/form-data':
					query = cgi.parse_multipart(self.rfile, pdict)
				
				self.send_response(301)

				self.end_headers()
				upfilecontent = query.get('upfile')
				
				webutils.log('filecontent', upfilecontent[0])
				
				self.wfile.write('<html>POST OK.<br><br></html>')
				self.wfile.write(upfilecontent[0])

			except Exception as e:
				webutils.log('The all-inclusive except')

		webutils.consoleDivider(length=85)


	def normaliseQuery(self, query):
	
		'''
		Parses and normalises a query string
	
		'''
	
		query = parse_qs(query, keep_blank_values=True, strict_parsing=False, encoding='UTF-8', errors='replace') # 

		return { 'ID'    : int(query['ID'][0]) if 'ID' in query else None,
		         'title' : query.get('title',  [None])[0],
		         'author': query.get('author', [None])[0]  }


	def interpolateEntryHTML(self, entry):
	
		'''
		Fills in an HTML template for a single entry.
	
		'''
	
		return entryTemplate.format(title=entry['title'], contents=entry['contents'], time=entry['date'], author=entry['author'])


	def handleDynamicRequest(self, contentType, request):

		'''
		Docstring goes here

		'''

		# TODO: Handle other dynamic requests (eg. JSON API requests)
		# TODO: Query types
		# TODO: Decode query components (html escapes)

		if request.path == '/entry.esp':

			# Request for a blog entry
			# TODO: Not sure if this (entry path) is the best approach
			# TODO: Handle errors

			# TODO: Extract some common functionality (eg. fetching rows and filling in templates)
			
			entries = [entry for entry in database.fetchEntries(connection, **self.normaliseQuery(request.query))]
			
			if len(entries) == 0:
				# Probably not the right course of action for a dynamic request
				response = '<html>404: Couldn\'t find what you asked for.</html>'
				self.send_error(404, 'File Not Found: %s' % request.path)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				webutils.sendUnicode(self.wfile, response)
			else:
				response = pageTemplate.format(title='Blog Posts', entries='\n'.join(self.interpolateEntryHTML(entry) for entry in entries))
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				webutils.sendUnicode(self.wfile, response)
		elif request.path == '/api.esp':

			# API
			entries  = [entry for entry in database.fetchEntries(connection, **self.normaliseQuery(request.query))]
			response = json.dumps([{ 'contents': self.interpolateEntryHTML(entry),
				                     'author':   entry['author'],
				                     'date':     entry['date']
				                   } for entry in entries])

			self.send_response(200)
			self.send_header('Content-type', 'application/json')
			self.end_headers()
			webutils.sendUnicode(self.wfile, response)

		else:
			# Some other request
			pass


	def handleContentRequest(self, contentType, request):

		'''
		Docstring goes here

		'''

		# The Holy Trinity (or plaintext)
		# TODO: Handle invalid paths
		filename = request.path[1:] # Relative path

		if not path.exists(filename):
			# Invalid path
			# TODO: Figure how how to handle paths properly (no ../, shave off initial slash, etc.)
			# TODO: What's the difference between send_error and send_response?
			webutils.log("404:", path.join(root, filename))
			self.error_message_format = '\n'.join(('<body>',
												   '<h1 style="background:red;">Error!</h1>',
												   '<p>Error code %(code)d.</p>',
												   '<p>Message: %(message)s.</p>',
												   '<p>Error code explanation: %(code)s = %(explain)s.</p>',
												   '</body>'))
			self.send_error(404, 'File Not Found: %s' % path.join(root, filename))
		else:
			with open(filename, 'rb') as f:
				self.send_response(200)
				self.send_header('Content-type', '{0:}/{1:}'.format(*contentType))
				self.end_headers()
				webutils.sendUnicode(self.wfile, f)


	def handleImageRequest(self, contentType, request):

		'''
		Docstring goes here
		
		'''

		# TODO: Handle invalid paths
		filename = request.path[1:]

		with open(filename, 'rb') as f:
			self.send_response(200)
			self.send_header('Content-type', contentType)
			self.end_headers()
			self.wfile.write(f.read())



	def handleDynamicPost(self, contentType, request):
	
		'''
		Docstring goes here
	
		'''

		if request.path == '/publish.esp':
			#
			webutils.log('Storing published entry...')
			size  = int(self.headers['content-length'])
			data  = self.rfile.read(size)
			entry = json.loads(data.decode(encoding='UTF-8'))
			database.storeEntry(connection, entry['title'], entry['contents'], entry['author']) # TODO: Author param should be verified (login)
			# TODO: Send response
			response = json.dumps({ 'status': 'OK' }).encode('UTF-8') # TODO: Send something useful...
			self.send_response(200)
			self.send_header('Content-type', 'application/json')
			self.send_header('Content-Length', len(response))
			self.end_headers()
			self.wfile.write(response)


	def handleInvalidRequest(self, verb, contentType, request):
	
		'''
		Docstring goes here
	
		'''
	
		if '.' not in self.path:
			# Not implemented response code
			self.send_error(501, 'Unable to handle your request at this moment.')
		else:
			webutils.log('I\'m not quite sure what went wrong. Sorry. This is all new to me.')


	def dispatch(self, verb, url):
	
		'''
		Verifies that an incoming request is valid and delegates the
		request handling to the proper method.
	
		'''
		
		# TODO: Cache the handler dictionaries
		# TODO: Best approach for request dispatch (request.path, headers, query, content type, etc.)	
		# TODO: Handler signature (rely on class attributes, or pass parameters)
		# TODO: Parse headers (?)

		# TODO: HTTP status codes

		# TODO: Figure out what esp really is

		assert verb in ('GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'TRACE', 'OPTIONS', 'CONNECT', 'PATCH'), 'Invalid verb (\'{verb}\')'.format(verb=verb) # Formally 'methods'

		#
		request     = ParseResult(*(unquote(part) for part in urlparse(self.path))) # Unpack url components and decode HTML escapes (%xx)
		contentType = webutils.contentTypeFromPath(request.path)                    # Content type

		webutils.log(contentType)

		# GET request handlers
		GET = {
			'dynamic': lambda ctype, req: self.handleDynamicRequest(ctype, req), #
			'text':    lambda ctype, req: self.handleContentRequest(ctype, req), #
			'image':   lambda ctype, req: self.handleImageRequest(ctype, req)    #
		}

		# POST request handlers
		POST = {
			'dynamic': lambda ctype, req: self.handleDynamicPost(ctype, req)
		}

		if verb == 'POST':
			POST.get(contentType.category, lambda ctype, req: self.handleInvalidRequest(verb, ctype, req))(contentType, request)
		elif verb == 'GET':
			GET.get(contentType.category, lambda ctype, req: self.handleInvalidRequest(verb, ctype, req))(contentType, request)
		else:
			raise NotImplementedError



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
		server = HTTPServer(('', port), Publisher)
		webutils.log('Started httpserver at port {port}...'.format(port=port))
		server.serve_forever()
	except KeyboardInterrupt:
		server.socket.close()



if __name__ == '__main__':
	main()