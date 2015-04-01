#
# main.py
# ...
#
# Jonatan H Sundqvist
# March 28 2015
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
#        - GUI
#          -- Swap request handlers at runtime (click and drag like puzzles)
#          -- Inspect server state
#
#        - Modulariy
#          -- Move the remaining server logic to server.py

# SPEC | -
#        -



import webutils #
import database #
import server

from SwiftUtils.SwiftUtils import ordinal # TEST

import json
from datetime import datetime

from os import path

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote, urlparse, parse_qs, ParseResult



def main():
	
	'''
	Docstring goes here

	'''

	server.create(port=80) # .serve_forever() # TODO: Provide separate serverForever function, renamed (?)



if __name__ == '__main__':
	main()