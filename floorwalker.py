#!/usr/bin/python

# Floorwalker is a simple tool to mirror Pastebin activity.
# Future planned functionality includes searching and alerting according to
# regular expressions.

from bs4 import BeautifulSoup

import sys
import urllib2

# Planning through commenting!

# instantiated thru cron so check for a lock first

# assuming nothing else is running, get http://pastebin.com/archive
testurl = "http;//pastebin.com/archive"

req = urllib2.Request(testurl)
try:
		response = urllib2.urlopen(req)
except URLError, e:
		if hasattr(e,'reason'):
				sys.stderr.write('urlopen() returned error '+e.reason+'\n')
		elif hasattr(e,'code'):
				sys.stderr.write('Server couldn\'t fulfill request: '+e.code+'\n')
		else:
				sys.stderr.write('Opened '+testurl+' with response code '+response.getcode()+'\n')

soup = BeautifulSoup(response)

# Generate list of pastes

# Iterate through each listed paste
# if we don't already have this one, store it
