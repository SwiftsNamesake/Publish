#
# webutils.py
# Various web related utilities
#
# Jonatan H Sundqvist
# March 28 2015
#

# TODO | - 
#        - 

# SPEC | -
#        -



from pprint import pprint # TEST
from os.path import splitext

from collections import namedtuple



# Maps file extensions to their respective content types
contentTypes = { ext : media for media, exts in {
	'text': 	('.html', '.css', '.js', '.txt'),
	'image': 	('.png', '.jpg', '.jpeg' '.gif', '.ico'),
	'dynamic': 	('.esp', )
}.items() for ext in exts }

ContentType = namedtuple('ContentType', 'category subtype') # Represents an internet media type (type and subtype)

print(pprint(contentTypes)) # TEST



def escapeUnicode(data):

	'''
	Returns escaped HTML from the specified UTF-8 encoded file or string

	'''

	data = { str: lambda: data, }.get(type(data), lambda: data.read().decode('UTF-8'))() # Couldn't resist a type switch
	return data.encode('ascii', 'xmlcharrefreplace')



def contentTypeFromPath(path):

	'''
	Determines the content type of a particular file path or URL,
	based on its extension.

	'''

	# TODO: Error handling
	# TODO: Use existing modules instead (?)

	# TODO: Spec compliance (https://en.wikipedia.org/wiki/Internet_media_type)

	ext = splitext(path)[-1]               # Extension
	cat = contentTypes.get(ext, 'unknown') # Category

	content = ({'.js': 'javascript', '.txt': 'plain'}).get(ext, ext[1:]) # Shave off dot

	# return '{category}/{exact}'.format(category=cat, exact=content)
	return ContentType(cat, content)



def sendUnicode(wfile, contents):

	'''
	Escapes Unicode text (provided as a string or file handle)
	and writes it to the provided write file (wfile).

	See webutils.escapeUnicode for details on HTML escaping. 

	'''

	# TODO: Error handling,return values
	wfile.write(escapeUnicode(contents))