#
# main.py
# ...
#
# Jonatan H Sundqvist
# March 28 2015
#

# TODO | - Robustness
#          -- Unit tests, dry runs
#          -- Static checks (?)
#
#        - Read up on the BaseHTTPRequestHandler class and networking in general
#        - Users (table in database)
#        - HTML utilities
#
#        - Modulariy
#          -- Move the remaining server logic to server.py

# SPEC | -
#        -



import webutils #
import database #
import server   #



def main():
	
	'''
	Docstring goes here

	'''

	server.create(port=350) # .serve_forever() # TODO: Provide separate serverForever function, renamed (?)



if __name__ == '__main__':
	main()