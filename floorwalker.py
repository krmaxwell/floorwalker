#!/usr/bin/python

# Floorwalker is a simple tool to mirror Pastebin activity.
# Future planned functionality includes searching and alerting according to
# regular expressions.

from bs4 import BeautifulSoup

import sys
import urllib2
import time

# Planning through commenting!

def geturl(myurl):
    req = urllib2.Request(myurl)
    # TODO: use proper loggging, not just stderr
    try:
        response = urllib2.urlopen(req)
    except urllib2.URLError, e:
        if hasattr(e,'reason'):
            sys.stderr.write('urlopen() returned error '+e.reason+'\n')
        elif hasattr(e,'code'):
            sys.stderr.write('Server couldn\'t fulfill request: '+e.code+'\n')
        else:
            sys.stderr.write('Opened '+testurl+' with response code '+response.getcode()+'\n')
    return response
    
# TODO: check for a lock first

testurl = "http://pastebin.com/archive"

# Just keep running until somebody tells us to stop
while True:
    # TODO: handle KeyboardError and kill commands
    response = geturl(testurl)

    # Generate list of pastes
    soup = BeautifulSoup(response)
    tabledata = soup.find_all('td')
    # TODO: pastes should be persistent across runs so we don't have to grab it every time
    pastes = []
    for td in tabledata:
        try:    
            if td.a['href'].count("/archive/") == 0:
            # TODO: use regex 
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
            time.sleep(2)
            pasteurl = 'http://pastebin.com/raw.php?i='+paste
            pasteresp = geturl(pasteurl)
            try:
            # TODO: replace with sqlite3
                pastefile=open('data/'+paste,'w')
                pastefile.write(pasteresp.read())
                pastefile.close()
            except:
                sys.stderr.write('ERMAGERD couldn\'t write to file: data/'+paste+'\n')
    time.sleep(60)
