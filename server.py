#
# server.py
# This is not a joke
#
# None
# April 01 2015
#

# TODO | - Logging (database, plain text)
#        - Security, privileges, encryption, https, hashes, salts, etc.
#          -- https://www.piware.de/2011/01/creating-an-https-server-in-python/
#
#        - API (restful)
#          -- Searching
#          -- Queries (by date, by title, by id, etc.)
#          -- Posting
#          -- Listing entries
#          -- JSON
#          -- Unify and standardise API
#
#        - Threading (?)
#        - Custom error pages
#
#        - Prevent server from stalling because of the console (eg. when selecting text)
#        - GUI
#          -- Swap request handlers at runtime (click and drag like puzzles)
#          -- Inspect server state

# SPEC | -
#        -



import webutils #
import database #

import json
import time

from datetime import datetime # TODO: Remove (?)
from os import path

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote, urlparse, parse_qs, ParseResult



# TODO: Close file properly
# TODO: Move initialisation code into separate function
pageTemplate  = open('pageTemplate.html',  'r', encoding='UTF-8').read()
entryTemplate = open('entrytemplate.html', 'r', encoding='UTF-8').read()

connection = database.createDatabase('site.db')         # TODO: Move this
database.createDummyEntries(connection, overwrite=True) # 

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

		print(self.server)

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
		
		# TODO: Handle errors
		# TODO: Keep up-to-date with the database schemas
		# TODO: Exclude None values (?)

		query = parse_qs(query, keep_blank_values=True, strict_parsing=False, encoding='UTF-8', errors='replace') # 

		return { key: value for key, value in { 'id'       : int(query['id'][0]) if 'id' in query else None,               # 
				                                'earliest' : float(query['earliest'][0]) if 'earliest' in query else None, # 
				                                'title'  : query.get('title',  [None])[0],                                 # 
				                                'userID' : query.get('userID', [None])[0]  }.items() if value is not None} # 


	def interpolateEntryHTML(self, entry):
	
		'''
		Fills in an HTML template for a single entry.
	
		'''

		# TODO: Error handling
		# TODO: More flexible HTML generation

		sobriquet = database.fetch(connection, 'users', where=('id={id}'.format(id=entry['userID']), )).fetchone()['sobriquet']

		return entryTemplate.format(title=entry['title'],
		                            contents=entry['contents'],
		                            time=webutils.localTimeFormat(entry['timestamp']),
		                            author=sobriquet)


	def handleDynamicRequest(self, contentType, request):

		'''
		Docstring goes here

		'''

		# TODO: Handle other dynamic requests (eg. JSON API requests)
		# TODO: Query types
		# TODO: Decode query components (html escapes)
		# TODO: Move API logic to separate method(s)
		# TODO: Validate query (omitting will case an assertion error in fetchEntries)

		query    = self.normaliseQuery(request.query) #
		earliest = query.pop('earliest', 0)           # datetime.strptime()

		if request.path == '/entry.esp':

			# Request for a blog entry
			# TODO: Not sure if this (entry path) is the best approach
			# TODO: Handle errors

			# TODO: Extract some common functionality (eg. fetching rows and filling in templates)
			# TODO: Should certain columns be hidden (eg. the id)

			where   = tuple('{k}={v}'.format(k=k, v=v) for k, v in query.items())
			rows    = database.fetch(connection, 'entries', where=where)

			entries = [entry for entry in rows]
			
			if len(entries) == 0:
				# Probably not the right course of action for a dynamic request
				response = '<html>404: Couldn\'t find what you asked for.</html>'
				self.send_error(404, 'File Not Found: %s' % request.path)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				webutils.sendUnicode(self.wfile, response)
			else:
				# response = pageTemplate.format(title='Blog Posts', entries='\n'.join(self.interpolateEntryHTML(entry) for entry in entries))
				response = pageTemplate.format(title='Blog Posts', entries='')

				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				webutils.sendUnicode(self.wfile, response)

		elif request.path == '/api.esp':

			# API
			# TODO: Non-stupid way of filtering by date (should be done with an SQL query)
			# webutils.log('earliest', earliest) # TODO: Causes memory error...

			where   = ('timestamp > %d' % int(earliest), ) + tuple('{k}={v}'.format(k=k, v=v) for k, v in query.items())
			entries = [entry for entry in database.fetch(connection, 'entries', where=where)]

			response = json.dumps([{ 'contents':  self.interpolateEntryHTML(entry),
				                     'author':    database.fetch(connection, 'users', where=('id=%d' % entry['userID'], )).fetchone()['sobriquet'],
				                     'timestamp': entry['timestamp'],
				                     'date':      webutils.localTimeFormat(entry['timestamp'])
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

		# TODO: Move reading and decoding to separate function (?)
		# TODO: JSON utilities (headers, content type, dumping and encoding, etc.)
		# TODO: Move API logic to separate method(s)

		if request.path == '/publish.esp':
			#
			webutils.log('Storing published entry...')
			size  = int(self.headers['content-length'])
			data  = self.rfile.read(size)
			entry = json.loads(data.decode(encoding='UTF-8'))
			# TODO: Security, no naive userID direct use
			# TODO: Author param should be verified (login)
			database.storeEntry(connection, entry['title'], entry['contents'], database.fetch(connection, 'users', where=('sobriquet=%r' % entry['author'], )).fetchone()['id'])

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

		# TODO: Clean up the naming of handlers (less ambiguous, more consistent)
		# TODO: Reconsider the dispatch logic (?)

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
			# 
			POST.get(contentType.category, lambda ctype, req: self.handleInvalidRequest(verb, ctype, req))(contentType, request)
		elif verb == 'GET':
			# 
			GET.get(contentType.category, lambda ctype, req: self.handleInvalidRequest(verb, ctype, req))(contentType, request)
		elif verb == 'HEAD':    raise NotImplementedError
		elif verb == 'PUT':     raise NotImplementedError
		elif verb == 'DELETE':  raise NotImplementedError
		elif verb == 'TRACE':   raise NotImplementedError
		elif verb == 'OPTIONS': raise NotImplementedError
		elif verb == 'CONNECT': raise NotImplementedError
		elif verb == 'PATCH':   raise NotImplementedError
		else:
			# TODO: This should never happen
			# TODO: This is probably not the best approach
			raise NotImplementedError



def create(port=80, handler=Publisher):

	'''
	Docstring goes here
	
	'''

	# TODO: Error handling
	# TODO: Rename arguments (esp. handler) (?)
	# TODO: Interrupt handler, promises (?)

	try:
		server = HTTPServer(('', port), handler)
		webutils.log('Started httpserver at port {port}...'.format(port=port))
		server.serve_forever()
	except KeyboardInterrupt:
		webutils.consoleDivider(length=85, header='Turning off the lights. Good night')
		server.socket.close()



def main():
	
	'''
	Docstring goes here

	'''

	pass



if __name__ == '__main__':
	main()