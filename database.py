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
#        - Read up on the SQL language
	
# SPEC | -
#        -



import sqlite3

from subprocess import call # For Git commands
from datetime import datetime
from collections import namedtuple


# (id real, date text, author text, title text, contents text)')
# TODO: Creating row schemas from namedtuples (?)
EntryRow = namedtuple('EntryRow', 'ID date author title contents') #
UserRow  = namedtuple('UserRow',  'ID joined sobriquet email username password')


DEBUG   = True
TESTING = True



def test(f):

	'''
	Test decorator

	'''

	# TODO: Accept arguments
	# TODO: Logging
	# TODO: Use wrapper decorator from functools

	def wrapper(*args, **kwargs):
		if TESTING: f(*args, **kwargs)
	wrapper.orignal = f
	return wrapper



@test
def createDummyEntries(connection, overwrite=False):

	'''
	Docstring goes here

	'''

	# TODO: Make sure IDs aren't reused (for actual content atleast)
	# TODO: Reserve a few IDs for testing (?)

	cursor  = connection.cursor()
	entries = (('Weather', 'I like sunshine.'), ('Politics', 'They\'re all evil.'), ('Computers', 'They scare me.'), ('Math', 'π is in fact 4.6.'))

	if overwrite:
		print('Deleting previous dummy entries...')
		cursor.execute('DELETE FROM entries WHERE id < ?', len(entries))

	if cursor.execute('SELECT Count(0) FROM entries').fetchone()[0] >= 4:
		print('Dummy entries have already been created')
		return

	print('Creating dummy entries...')

	for title, text in entries:
		#(id real, date text, author text, title text, contents text)
		storeEntry(connection, title, text, 'Jonatan H Sundqvist')

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

	print('Connecting to database ({path})...'.format(path=databasePath))

	connection = sqlite3.connect(databasePath)
	cursor     = connection.cursor()

	connection.row_factory = sqlite3.Row #lambda cur, row: EntryRow(*row) if len(row) == 5 else row # TODO: Make configurable, move to separate function

	# TODO: Check table format too (not just existence)
	# TODO: Decide on a table schema

	cursor.execute('CREATE TABLE IF NOT EXISTS entries (id integer, date text, author text, title text, contents text)') # Create the entries table if it does not already exist
	connection.commit()

	return connection



def executeAndCommit(connection, statement, parameters=tuple()):

	'''
	Executes and commits a single SQL statement with the provided connection,
	possibly with a tuple of parameters to interpolate. Returns the cursor.

	'''

	# TODO: Handle errors
	cursor = connection.cursor()
	cursor = cursor.exexute(statement, parameters)
	connection.commit()

	return cursor



def fetchEntries(connection, title=None, ID=None, author=None):

	'''
	Fetches all entries matching the given query.
	Ignoring all parameters will result in an assertion error.

	Entries with identical titles are (currently) allowed, though
	all but the first will be omitted from the result.

	'''

	# TODO: Only ONE argument is used for the query (currently)
	# TODO: Allow customised queries, more than one attribute
	# TODO: Generalise (query by row values for other tables) (use kwargs?)
	# TODO: Performance

	arguments = (title, ID, author)

	assert any(attr is not None for attr in arguments), 'Whoops. You forgot to supply an argument (either a title, an ID, or an author will do)'

	specified = next(attr for attr in arguments if attr is not None )

	attribute = {
		title:  'title',
		ID:     'id',
		author: 'author'
	}[specified]

	cursor = connection.cursor()
	cursor.execute('SELECT * FROM entries WHERE {attribute}=?'.format(attribute=attribute), (specified, )) #

	return cursor



def fetchEntry(connection, title=None, ID=None):

	'''
	Fetches a single entry based on its title or ID.
	Ignoring both parameters will result in an assertion error.

	Entries with identical titles are (currently) allowed, though
	all but the first will be omitted from the result.

	'''

	return fetchEntries(connection, title=title, ID=ID).fetchone()



def storeEntry(connection, title, text, author):

	'''
	Docstring goes here

	'''

	# TODO: Rename (?)
	# TODO: Decide on how to handle time stamps (locale, time zone, format, etc.)
	# TODO: Proper ID handling
	# TODO: Commit (?)

	cursor   = connection.cursor()
	rowcount = cursor.execute('SELECT Count(*) FROM entries').fetchone()[0] #
	cursor.execute('INSERT INTO entries VALUES (?, ?, ?, ?, ?)', (rowcount, datetime.now().strftime('%c'), author, title, text))



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