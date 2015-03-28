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

# SPEC | -
#        -



import sqlite3
from subprocess import call # For Git commands



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

	connection = sqlite3.connect(self.databasePath)
	cursor     = connection.cursor()

	# TODO: Check table format too (not just existence)
	# TODO: Decide on a table schema

	cursor.execute('CREATE TABLE IF NOT EXISTS entries (id real, date text, author text, title text, contents text)') # Create the entries table if it does not already exist
	conn.commit()

	return connection



def fetchEntry(cursor, title=None, ID=None):

	'''
	Fetches a single entry based on its title or ID.
	Ignoring both parameters will result in an assertion error.

	Entries with identical titles are (currently) allowed, though
	all but the first will be omitted from the result.

	'''

	assert (title, ID) != (None, None), 'Whoops. You forgot to supply an argument (either a title or an ID will do)'
	cursor.execute('SELECT * FROM entries WHERE {attribute}=?'.format(attribute='title' if title else 'id'), title or ID) #
	return cursor.fetchone()


def storeEntry():

	'''
	Docstring goes here

	'''

	# TODO: Rename (?)
	
	pass



def commitDatabaseChanges(path):

	'''
	Docstring goes here

	'''

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