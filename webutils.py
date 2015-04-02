#
# webutils.py
# Various web related utilities
#
# Jonatan H Sundqvist
# March 28 2015
#

# TODO | - Rename to utils.py or separate web utilities from common utilities
#        - 

# SPEC | -
#        -



import time

from pprint import pprint # TEST
from os.path import splitext

from collections import namedtuple
from datetime import datetime



# Maps file extensions to their respective content types
contentTypes = { ext : media for media, exts in {
	'text': 	('.html', '.css', '.js', '.txt'),
	'image': 	('.png', '.jpg', '.jpeg' '.gif', '.ico'),
	'dynamic': 	('.esp', )
}.items() for ext in exts }

ContentType = namedtuple('ContentType', 'category subtype') # Represents an internet media type (type and subtype)



def consoleDivider(length=80, header='', padx=' '):

	'''
	Prints a divider with an optional heading.

	'''

	# TODO: Option for closing dividers and indentation withing a console section
	# TODO: Fancy console output (?)

	padLen     = 2 * len(padx) * len(header[:1])  # Padding on each side of the header
	headerLen  = len(header)                      #
	indent     = 2                                # Indentation of the header
	dividerLen = length-(padLen+headerLen+indent) #o

	print('\n\n{indent}{padx}{header}{padx}{divider}\n\n'.format(indent=indent*'-', padx=padx*len(header[:1]), header=header, divider='-' * dividerLen))


def log(message, indent=2):

	'''
	Prints a simple log message.

	'''

	print('{indent}{message}'.format(indent=(' ' * indent), message=message))


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



def replace(text, instead, begin, end):
	
	'''
	Replaces a portion of a string (or any object supporting slices and concatenation)

	'''

	return text[:begin] + instead + text[end:]



def toUTCSeconds(date):

	'''
	Converts a local-specific datetime string to an epoch
	timestamp (seconds since January 1, 1970)

	'''

	# TODO: Remove this or reimplement with time module (datetime has timezone issues, it seems)
	# TODO: Direct support datetime arguments
	# TODO: Rename (eg. something related to epoch, seconds since)

	return (datetime.strptime(date, '%c') - datetime.fromtimestamp(0)).total_seconds()



def showUTCOffset(timestamp, timezone):

	'''
	Converts a timestamp to a UTC offset string (UTC[+|-]hhmm).

	'''

	# TODO: Error handling

	# Time zone offset from UTC+0000 (Universal Coordinate Time)
	# The negation is necessary (or atleast convenient) because
	# the timezone is given as (UTC - local), meaning that positive
	# offsets will be represented (eg. UTC+0100) by a negative value (eg. -3600)
	offset = -timezone # Time zone offset (seconds)

	# Simplify hh and mm calculations (some clever divmod trickery, perhaps?)
	sign = ('+', '-')[offset < 0] #
	hh   = (offset // 3600)       #
	mm   = (offset % 3600)//60    #

	return  'UTC{sign}{hh:02d}{mm:02d}'.format(sign=sign, hh=hh, mm=mm) # TODO: Use existing utility instead (UTC[+|-]hhmm)



def localTimeFormat(timestamp):

	'''
	Converts a timestamp (seconds since the epoch inception) to a
	locale-specific time string.

	'''

	# TODO: Use datetime or time for strftime (?)
	# TODO: Use a standard format instead (eg. dd/mm/yyyy hh:mm:ss UTC[+|-]hhmm)

	# time.strftime doesn't seem to handle %c correctly

	return time.strftime('%c {timezone}'.format(timezone=showUTCOffset(timestamp, time.timezone)), time.localtime(timestamp))



def articleOf(noun):

	'''
	Decides which article (a or an) a noun should have based
	on its first letter (vowel or consonant).

	'''

	# TODO: Take pronunciation into account

	return 'an' if noun[0].lower() in 'aeiou' else 'a'



def assertInstance(name, value, thetype):

	'''
	Docstring goes here

	'''

	# Yes, grammar is that important
	actual = str(type(value))
	assert isinstance(value, thetype), '{name} must be {ideal} (not {actual})'.format(name=name,
	                                                                                  ideal=webutils.articleOf(str(thetype)) + ' ' + str(thetype),
	                                                                                  actual=webutils.articleOf(actual) + ' ' + actual)
