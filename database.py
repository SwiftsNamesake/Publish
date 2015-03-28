#
# database.py
# ...
#
# Jonatan H Sundqvist
# March 28 2015
#

# TODO | - Close connection in between operations (?)
#        - Keep cursor or create new ones (?)
#        - Choosing unique IDs
#        - Friendlier API (eg. using row factory to create namedtuple rows)
#        - Don't hardcode database parameters (eg. schema and table name) 
#        - Decide on how to handle time stamps (locale, time zone, format, etc.)
	
# SPEC | -
#        -



import sqlite3

from subprocess import call # For Git commands
from datetime import date



def test(f):

	'''
	Test decorator

	'''

	# TODO: Accept arguments
	# TODO: Logging
	# TODO: Use wrapper decorator from functools

	def wrapper(*args, **kwargs):
		if True: f(*args, **kwargs)
	wrapper.orignal = f
	return wrapper



@test
def createDummyEntries(connection):

	'''
	Docstring goes here

	'''

	# TODO: Make sure IDs aren't reused (for actual content atleast)
	# TODO: Reserve a few IDs for testing (?)

	cursor = connection.cursor()

	for title, text in (('Weather', 'I like sunshine.'), ('Politics', 'They\'re all evil.'), ('Computers', 'They scare me.'), ('Math', 'π is in fact 4.6.')):
		#(id real, date text, author text, title text, contents text)
		storeEntry(connection, title, text)

	connection.commit()



def configure(self):

	'''
	Docstring goes here

	'''

	self.databasePath = None #
	self.database     = None #



def createDatabase(databasePath):

	'''
	Creates the database and the entries table if they do not already exist,
	and returns the connection.

	'''

	connection = sqlite3.connect(databasePath)
	cursor     = connection.cursor()

	# TODO: Check table format too (not just existence)
	# TODO: Decide on a table schema

	cursor.execute('CREATE TABLE IF NOT EXISTS entries (id real, date text, author text, title text, contents text)') # Create the entries table if it does not already exist
	connection.commit()

	return connection



def fetchEntry(connection, title=None, ID=None):

	'''
	Fetches a single entry based on its title or ID.
	Ignoring both parameters will result in an assertion error.

	Entries with identical titles are (currently) allowed, though
	all but the first will be omitted from the result.

	'''

	assert (title, ID) != (None, None), 'Whoops. You forgot to supply an argument (either a title or an ID will do)'
	cursor = connection.cursor()
	print('SELECT * FROM entries WHERE {attribute}={ID}'.format(attribute='title' if title else 'id', ID=ID))
	print(title, type(ID))
	print(title or ID)
	cursor.execute('SELECT * FROM entries WHERE {attribute}=?'.format(attribute='title' if title else 'id'), (title or ID, )) #
	return cursor.fetchone()



def storeEntry(connection, title, text):

	'''
	Docstring goes here

	'''

	# TODO: Rename (?)
	# TODO: Decide on how to handle time stamps (locale, time zone, format, etc.)
	# TODO: Proper ID handling
	# TODO: Commit (?)

	cursor   = connection.cursor()
	rowcount = cursor.execute('SELECT Count(*) FROM entries').fetchone()[0] #
	cursor.execute('INSERT INTO entries VALUES (?, ?, ?, ?, ?)', (rowcount, date.today().strftime('%c'), 'Jonatan H Sundqvist', title, text))



def commitDatabaseChanges(path):

	'''
	Docstring goes here

	'''

	# TODO: Rename (confusion between git commit/connection commit) (?)
	# TODO: Error handling (eg. invalid path, wrong, directory)
	subprocess.call('git add "{path}"'.format(path=path))                                                          #
	subprocess.call('git commit "{path}" -m "{message}"'.format(path=path, message='Committing database changes')) # TODO: More informative commit message



def main():

	'''
	Docstring goes here

	'''

	pass



if __name__ == '__main__':
	main()