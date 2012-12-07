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
import pymongo
from dateutil.parser import *
from dateutil.tz import *
from datetime import *

# Planning through commenting!

def getpaste(pasteID):
    pastepage = geturl('http://pastebin.com/'+pasteID)
    # now parse this and return a dict
    mysoup = BeautifulSoup(pastepage)
    title = mysoup.title.text
    author = mysoup.find_all('div', 'paste_box_line2')[0].a.text
    line = mysoup.find_all('div', 'paste_box_line2')[0].text
    mydate = parse(line.split(' ')[4] + line.split(' ')[5] +line.split(' ')[6])
    pastetext = BeautifulSoup(geturl('http://pastebin.com/raw.php?i='+pasteID)).text
    fullpaste = {'title': title, 'author': author, 'date': mydate.strftime("%Y-%m-%d") , 'paste': pastetext}
    return fullpaste

def geturl(myurl):
    req = urllib2.Request(myurl)
    try:
        response = urllib2.urlopen(req)
        return response
    except urllib2.URLError, e:
        if hasattr(e,'reason'):
            logging.warning('urlopen() returned error %s\n',e.reason)
        elif hasattr(e,'code'):
            logging.warning('Server couldn\'t fulfill request: %s\n',e.code)
        else:
            logging.warning('Opened %s with response code %s',myurl,response.getcode())
    
# TODO: check for a lock first
if __name__="__main__":
    logging.basicConfig(filename='floorwalker.log',format='%(asctime)s %(message)s',datefmt='%Y-%m-%d %H%M.%S',level=logging.DEBUG)
    archiveurl = "http://pastebin.com/archive"
    pastere = re.compile("\w")

    # connect to mongodb
    connection = pymongo.MongoClient
    db = connection.floorwalker
    pastes = db.pastes

    # TODO: handle KeyboardError and kill commands
    logging.info('Getting URL %s', archiveurl)
    response = geturl(archiveurl)

    # Generate list of pastes
    soup = BeautifulSoup(response)

    # Be nice if we're going too fast
    if soup.get_text().find('Please slow down'):
        time.sleep(10)
    
    tabledata = soup.find_all('td')
    for td in tabledata:
        # TODO: rewrite without the try/except using hasattr()
        if hasattr(td.a['href'], count) and td.a['href'].count("/archive/") == 0:
            # drop the leading "/"
            nextpasteID = td.a['href'][1::]
            logging.info('Found ref to paste %s', nextpasteID)
            if not havepaste(nextpasteID):
                paste = getpaste(nextpasteID)
    
        # Iterate through each listed paste
        # if we don't already have this one, store it
        for pasteID in pastes:
            pastematch = pastere.match(pasteID)
            paste = []
            havepaste = # result of checking for key in mongodb
    
    
            # nested try blocks feel bad, man
            if not havepaste:
                time.sleep(2)
                pasteurl = 'http://pastebin.com/raw.php?i='+pasteID
                logging.info('Getting paste %s', pasteID)
                pasteresp = geturl(pasteurl)
                if hasattr(pasteresp, '__read__'):
                    paste = pasteresp.read()
                    if paste.find('Please slow down'):
                        time.sleep(10)
                try:
                # TODO: replace with sqlite3
                    pastefile=open('data/'+pasteID,'w')
                    pastefile.write(paste)
                    pastefile.close()
                except:
                    logging.error('ERMAGERD couldn\'t write to file: data/'+pasteID+'\n')
        time.sleep(60)
