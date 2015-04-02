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
#        - Don't hardcode database parameters (eg. schema and table name) (...)
#
#        - Decide on how to handle time stamps (locale, time zone, format, seconds as int or string, etc.)
#          -- Leaning towards UTC-0 timestamps (seconds since midnight on January 1 1970)
#          -- Make sure the database, server and front-end have a consistent view of dates (eg. using the same format or knowing how to convert)
#          -- Normalise and verify epochs (or is it always Jan 1 1970 00:00) (?)
#
#        - Read up on the SQL language
#          -- Syntax highlighting (?)
#          -- Static grammar and semantic checks (eg. type safety)
#
#        - Read up on the sqlite3 module
#          -- How exactly does interpolation work (just for values, or grammar too?) (?)
#
#        - Integrity
#          -- Print debug information (changed rows, row count, etc.)
#          -- Sanitise all input, provide utilities for this which enforce security
#          -- Sanitise dynamic SQL queries
#          -- Wrap every transaction in a context manager (with) for automatic rollbacks
#          -- Prevent duplicates (IDs, users)
#          -- Integrate version control
#        
#        - API
#          -- Wrap queries in functions
#          -- Abstract types, formats, order, etc of tables (no leaking db internals)
#          -- Explain API
#          -- General utilities: addTable(schema), insertIntoTable(values), count, etc.
#
#        - Dynamic queries
#          - Create utilities for assembling queries with optional clauses

# SPEC | -
#        -



import webutils

import sqlite3 #
import time    #

from subprocess import call        # For Git commands
from collections import namedtuple # 


# (id real, date text, author text, title text, contents text)')
# TODO: Creating row schemas from namedtuples (?)
# EntryRow = namedtuple('EntryRow', 'ID timestamp author title contents') #
# UserRow  = namedtuple('UserRow',  'ID joined sobriquet email username password')

DEBUG   = True
TESTING = True



class Schemas(object):
	# TODO: Prevent tampering
	# TODO: Verify schemas
	# TODO: Schema utilities
	# TODO: Schema interpolation formats (:= syntax?)
	entries = '(id integer, timestamp integer, userID integer, title text, contents text)'
	users   = '(id integer, joined integer,    sobriquet text, email text, username text, passhash integer)'



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

	#
	cursor  = connection.cursor()
	entries = (('Weather', 'I like sunshine.'), ('Politics', 'They\'re all evil.'), ('Computers', 'They scare me.'), ('Math', 'π is in fact 4.6.'))
	users   = (('Jonatan H Sundqvist', 'my@email.com', 'swifty', 0), ) # TODO: WARNING, horrible password hash, just for testing

	#
	if overwrite:
		webutils.log('Deleting previous dummy entries...')
		cursor.execute('DELETE FROM entries WHERE id < ?', (len(entries), ))
		webutils.log('Deleted {count} entries'.format(count=cursor.rowcount))

		webutils.log('Deleting previous dummy users...')
		cursor.execute('DELETE FROM users WHERE id < ?', (len(users), ))
		webutils.log('Deleted {count} users'.format(count=cursor.rowcount))


	if cursor.execute('SELECT Count(0) FROM users WHERE id < ?', (len(users), )).fetchone()[0] >= len(users):
		webutils.log('Dummy users have already been created')
	else:
		webutils.log('Creating dummy users...')
		for sobriquet, email, username, passhash in users:
			storeUser(connection, sobriquet, email, username, passhash)


	if cursor.execute('SELECT Count(0) FROM entries WHERE id < ?', (len(entries), )).fetchone()[0] >= len(entries):
		webutils.log('Dummy entries have already been created')
	else:
		webutils.log('Creating dummy entries...')
		for title, text in entries:
			storeEntry(connection, title, text, cursor.execute('SELECT id FROM users WHERE sobriquet="Jonatan H Sundqvist"').fetchone()['id']) # TODO: Not sure about the syntax


	# TODO: Mute tests
	for entry in fetch(connection, 'entries'):
		print(*('%s=%s' % (k, str(entry[k]).encode('ascii', errors='replace')) for k in entry.keys()))

	for user in fetch(connection, 'users'):
		print(*('%s=%s' % (k, user[k]) for k in user.keys()))

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

	webutils.log('Connecting to database ({path})...'.format(path=databasePath))

	connection = sqlite3.connect(databasePath)

	connection.row_factory = sqlite3.Row #lambda cur, row: EntryRow(*row) if len(row) == 5 else row # TODO: Make configurable, move to separate function

	# TODO: Check table format too (not just existence)
	# TODO: Decide on a table schema

	# Create the entries table if it does not already exist
	with connection as cursor:
		cursor.execute('CREATE TABLE IF NOT EXISTS entries {schema}'.format(schema=Schemas.entries))
		cursor.execute('CREATE TABLE IF NOT EXISTS users   {schema}'.format(schema=Schemas.users))

	return connection



def executeAndCommit(connection, statement, parameters=tuple()):

	'''
	Executes and commits a single SQL statement with the provided connection,
	possibly with a tuple of parameters to interpolate. Returns the cursor.

	'''

	# TODO: Handle errors
	# TODO: Add promises (fail, support, progress)
	# TODO: Replace parameters with *parameters or *values

	with connection as cursor:
		cursor.execute(statement, parameters)
		return cursor



def fetchEntries(connection, title=None, ID=None, userID=None, limit=None):

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

	# TODO: Fix author query (now userID)

	arguments = (title, ID, author)

	assert any(attr is not None for attr in arguments), 'Whoops. You forgot to supply an argument (either a title, an ID, or an author ID will do)'

	specified = next(attr for attr in arguments if attr is not None)

	attribute = {
		title:  'title',
		ID:     'id',
		author: 'author'
	}[specified]

	with connection as cursor:
		cursor.execute(addOptionalClause('SELECT * FROM entries WHERE {attribute}=?', 'LIMIT', limit).format(attribute=attribute), (specified, )) #
		return cursor



def fetch(connection, table, where=None, limit=None):

	'''
	Fetches all rows from the given table that matches the query.
	Currently supports the WHERE and LIMIT clause.

	'''

	# TODO: Column select (susceptible to injections?)
	# TODO: Sanitise input
	# TODO: Use dictionary instead, treat escaping properly

	# TODO: Accept where as single value too (no ugly singleton tuples)

	with connection:
		cursor = connection.cursor()
		# print('Where:', *where)
		where = '' if where is None else ' WHERE {constraints}'.format(constraints=' AND '.join(str(constraint) for constraint in where))
		limit = '' if limit is None else ' LIMIT {limit!s}'.format(limit=limit)
		query = 'SELECT * FROM {table}{where}{limit}'.format(table=table, where=where, limit=limit)
		print(query)
		cursor.execute(query)
		return cursor



def fetchRecent(connection, limit=None, earliest=None):

	'''
	Docstring goes here

	'''

	# TODO: User context managers more often
	# TODO: Check errors, exceptions, add logging
	# TODO: Utilities for assembling queries (including conditional clauses; eg. the LIMIT clause should only be included
	# when the corresponding parameter is not None)
	
	webutils.assertInstance('Limit', limit or 0, int)
	webutils.assertInstance('Earliest', earliest or 0, int)

	with connection as cursor:
		cursor.execute(addOptionalClause('SELECT * FROM entries WHERE timestamp > ?', 'LIMIT', limit), (earliest or 0, ))



def fetchEntry(connection, title=None, ID=None):

	'''
	Fetches a single entry based on its title or ID.
	Ignoring both parameters will result in an assertion error.

	Entries with identical titles are (currently) allowed, though
	all but the first will be omitted from the result.

	'''

	return fetchEntries(connection, title=title, ID=ID, limit=1).fetchone() # TODO: Use limit clause instead



def storeEntry(connection, title, text, userID):

	'''
	Docstring goes here

	'''

	# TODO: Rename (?)
	# TODO: Decide on how to handle time stamps (locale, time zone, format, etc.)
	# TODO: Proper ID handling (IMPORTANT, author is now an id for a user entry)

	# TODO: Generic store[Entry|Use|etc.] function

	with connection as cursor:
		rowcount = cursor.execute('SELECT Count(*) FROM entries').fetchone()[0] #
		cursor.execute('INSERT INTO entries VALUES (?, ?, ?, ?, ?)', (rowcount, int(time.time()), userID, title, text)) # TODO: See header for notes on timestamps



def storeUser(connection, sobriquet, email, username, passhash):

	'''
	Docstring goes here

	'''

	# TODO: Rename (?)
	# TODO: See also database.storeEntry
	# TODO: Sanitise, verify (eg. email) and handle errors

	with connection as cursor:
		# TODO: See header for notes on timestamps
		rowcount = cursor.execute('SELECT Count(*) FROM users').fetchone()[0] #
		cursor.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)', (rowcount, int(time.time()), sobriquet, email, username, passhash))



def commitChanges(path):

	'''
	Docstring goes here

	'''

	# TODO: Rename (confusion between git commit/connection commit) (?)
	# TODO: Error handling (eg. invalid path, wrong, directory)
	subprocess.call('git add "{path}"'.format(path=path))                                                          #
	subprocess.call('git commit "{path}" -m "{message}"'.format(path=path, message='Committing database changes')) # TODO: More informative commit message



def addOptionalClause(query, clause, value):

	'''
	Appends the specified clause to the query if the
	value is not None.

	'''

	# TODO: Change signatue (make clause the ENTIRE clause, replace value with include/exclude flag)
	# TODO: More succinct way of doing 'conditional formatting'
	# TODO: Error handling, sanitising
	# TODO: Verify syntax, allow more complex optional queries (currently just KEYWORD value at the end of the string)

	if value is None:
		return query
	else:
		return '{original} {optional}'.format(original=query, optional='{keyword} {value}'.format(keyword=clause, value=value)) 



def main():

	'''
	Docstring goes here

	'''

	pass



if __name__ == '__main__':
	main()