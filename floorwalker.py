#!/usr/bin/python

# Floorwalker is a simple tool to mirror Pastebin activity.
# Future planned functionality includes searching and alerting according to
# regular expressions.

from bs4 import BeautifulSoup

import sys
import urllib2

# Planning through commenting!

# TODO: instantiated thru cron so check for a lock first

# assuming nothing else is running, get http://pastebin.com/archive
testurl = "http://pastebin.com/archive"

req = urllib2.Request(testurl)
# TODO: factor out these urlopens and error checking
try:
    response = urllib2.urlopen(req)
except URLError, e:
    if hasattr(e,'reason'):
        sys.stderr.write('urlopen() returned error '+e.reason+'\n')
    elif hasattr(e,'code'):
        sys.stderr.write('Server couldn\'t fulfill request: '+e.code+'\n')
    else:
        sys.stderr.write('Opened '+testurl+' with response code '+response.getcode()+'\n')

# Generate list of pastes
soup = BeautifulSoup(response)
tabledata = soup.find_all('td')
pastes = []
for td in tabledata:
    try:    
        if td.a['href'].count("/archive/") == 0:
                pastes.append(td.a['href'])
    except:
        pass

# Iterate through each listed paste
# if we don't already have this one, store it
for paste in pastes:
    # drop the leading "/"
    paste = paste[1::]
    havepaste = True
    try:
        open('data/'+paste)
    except:
    	havepaste = False

    # nested try blocks feel bad, man
    if not havepaste:
        pasteurl = 'http://pastebin.com/raw.php?i='+paste
    	pastereq = urllib2.Request(pasteurl)
    	try:
    	    pasteresp = urllib2.urlopen(pastereq)
    	except URLError, e:
    	    if hasattr(e,'reason'):
    			sys.stderr.write('urlopen() returned error '+e.reason+'\n')
    	    elif hasattr(e,'code'):
    			sys.stderr.write('Server couldn\'t fulfill request: '+e.code+'\n')
    	    else:
    			sys.stderr.write('Opened '+testurl+' with response code '+response.getcode()+'\n')
    	try:
    		pastefile=open('data/'+paste,'w')
    		pastefile.write(pasteresp.read())
    		pastefile.close()
    	except:
    		sys.stderr.write('ERMAGERD couldn\'t write to file: data/'+paste+'\n')
 
