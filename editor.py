#
# editor.py
# A front end for the blog
#
# Jonatan H Sundqvist
# March 28 2015
#

# TODO | - POST requests
#        - Versioning (git, viewing diffs, etc.)
#        - Security, logins (cf. related TODOs in main.py)
#          -- Sanitise input (guard against SQL, HTML and JavaScript injections)
#
#        - Networking GUI
#          -- Use a queue (to prevent freezing)
#          -- Show 
#
#        - Editing features
#          -- Markup, advanced formatting

# SPEC | -
#        -



import webutils

import datetime
import urllib.request as request
import json

import tkinter as tk
import tkinter.ttk as ttk



def publish(entry):

	'''
	Docstring goes here

	'''

	# TODO: Allow file input
	# TODO: Validate data
	# TODO: Decide on a url format
	# TODO: Handle response
	# TODO: URL-escape

	# TODO: Promises, success/failure callbacks

	webutils.log('Publishing entry...')
	print(entry['contents'])

	try:
		headers = { 'content-type': 'application/json;charset=utf-8' }
		data    = json.dumps(entry).encode('UTF-8') # TODO: URL-encode this (?)
		url     = 'http://localhost:350/publish.esp'

		req      = request.Request(url, data=data, headers=headers, method='POST')
		response = request.urlopen(req).read().decode('UTF-8', 'ignore')
		
		print(response)
	except Exception as e:
		webutils.log('Something went wrong when trying to publish your entry:')
		webutils.log(e)



def createEditor():

	'''
	Docstring goes here

	'''

	size = (420, 420) 

	frame = tk.Tk()
	frame.title('New blog post...')
	# frame.geometry('{0}x{1}'.format(*size))

	title  = ttk.Entry()
	body   = tk.Text() # TODO: Text area
	auth   = ttk.Entry() #
	submit = ttk.Button(text='Publish', command=lambda: publish({'title': title.get(), 'contents': body.get('0.0', tk.END), 'author': auth.get()}))

	title.insert(0, 'Title...')
	body.insert(tk.INSERT, 'Body...')
	auth.insert(0, 'Author...')

	title.grid(row=0, column=0, columnspan=3, padx=4, pady=4, sticky=tk.W+tk.E)
	body.grid(row=1,  column=0, columnspan=3, padx=4, pady=4, sticky=tk.W+tk.E)
	auth.grid(row=2,  column=0, columnspan=2, padx=4, pady=4, sticky=tk.W+tk.E)

	submit.grid(row=2, column=2, columnspan=1, padx=4, pady=4, sticky=tk.W+tk.E)

	return frame



def main():

	'''
	Docstring goes here

	'''

	# publish({'author': 'Jonatan H Sundqvist', 'title': 'A New Beginning', 'contents': 'Listen carefully, this is very important.'})
	editor = createEditor()
	editor.mainloop()



if __name__ == '__main__':
	main()