#!/usr/bin/python

# Floorwalker is a simple tool to mirror Pastebin activity.
# Future planned functionality includes searching and alerting according to
# regular expressions.

from bs4 import BeautifulSoup

import sys
import urllib2
import time
import re
import logging

# Planning through commenting!

def geturl(myurl):
    req = urllib2.Request(myurl)
    try:
        response = urllib2.urlopen(req)
    except URLError, e:
        if hasattr(e,'reason'):
            logging.warning('urlopen() returned error '+e.reason+'\n')
        elif hasattr(e,'code'):
            logging.warning('Server couldn\'t fulfill request: '+e.code+'\n')
        else:
            logging.warning('Opened '+testurl+' with response code '+response.getcode()+'\n')
    return response
    
# TODO: check for a lock first

logging.basicConfig(filename='floorwalker.log',format='%(asctime)s %(message)s',datefmt='%Y-%m-%d %H%M.%S',level=logging.DEBUG)
testurl = "http://pastebin.com/archive"
pastere = re.compile("\w")

# Just keep running until somebody tells us to stop
while True:
    # TODO: handle KeyboardError and kill commands
    logging.info('Getting URL %s', testurl)
    response = geturl(testurl)

    # Generate list of pastes
    soup = BeautifulSoup(response)
    tabledata = soup.find_all('td')
    # TODO: pastes should be persistent across runs so we don't have to grab it every time
    pastes = []
    for td in tabledata:
        try:    
            if td.a['href'].count("/archive/") == 0:
                logging.info('Found ref to paste %s', td.a['href'])
                pastes.append(td.a['href'])
        except:
            pass

    # Iterate through each listed paste
    # if we don't already have this one, store it
    for paste in pastes:
        # drop the leading "/"
        pastematch = pastere.match(paste[1::])
        if pastematch:
            havepaste = True
            try:
                open('data/'+paste)
                logging.info('Found paste %s in data', pastematch.group())
            except:
                havepaste = False
        else:
            havepaste = True
            logging.info('Paste %s doesn\'t match the pattern', paste)

        # nested try blocks feel bad, man
        if not havepaste:
            time.sleep(2)
            pasteurl = 'http://pastebin.com/raw.php?i='+paste
            logging.info('Getting paste %s', paste)
            pasteresp = geturl(pasteurl)
            try:
            # TODO: replace with sqlite3
                pastefile=open('data/'+paste,'w')
                pastefile.write(pasteresp.read())
                pastefile.close()
            except:
                logging.error('ERMAGERD couldn\'t write to file: data/'+paste+'\n')
    time.sleep(60)
