#!/usr/bin/python

# Floorwalker is a simple tool to mirror Pastebin activity.
# Future planned functionality includes searching and alerting according to
# regular expressions.

'''
Copyright 2012 Kyle Maxwell

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from bs4 import BeautifulSoup

import sys
import urllib2
import re
import logging
import pymongo
from dateutil.parser import *
from dateutil.tz import *
from datetime import *
from time import sleep

def getpaste(pasteID):
    pastepage = geturl('http://pastebin.com/'+pasteID)
    # now parse this and return a dict
    fullpaste={}
    if pastepage:
        mysoup = BeautifulSoup(pastepage)
        title = mysoup.title.text
        if "Private Paste ID" not in title:
            author = mysoup.find_all('div', 'paste_box_line2')[0].a.text
            line = mysoup.find_all('div', 'paste_box_line2')[0].text
            tempdate = line.split('on')[1].split(' ')
            mydate = parse(tempdate[1] + tempdate[2] + tempdate[3])
            pastetext = BeautifulSoup(geturl('http://pastebin.com/raw.php?i='+pasteID)).text
            fullpaste = {'id': pasteID, 'title': title, 'author': author, 'date': mydate.strftime("%Y-%m-%d") , 'paste': pastetext}
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
if __name__=="__main__":
    logging.basicConfig(filename='floorwalker.log',format='%(asctime)s %(message)s',datefmt='%Y-%m-%d %H%M.%S',level=logging.DEBUG)
    archiveurl = "http://pastebin.com/archive"
    pastere = re.compile("\w")

    # connect to mongodb
    # TODO: error handling
    connection = pymongo.MongoClient()
    db = connection.floorwalker
    pastes = db.pastes

    # TODO: handle KeyboardError and kill commands
    logging.info('Getting URL %s', archiveurl)
    response = geturl(archiveurl)

    # Generate list of pastes
    soup = BeautifulSoup(response)

    # Be nice if we're going too fast
    if soup.get_text().find('Please slow down'):
        sleep(4)
    
    tabledata = soup.find_all('td')
    for td in tabledata:
        # TODO: rewrite without the try/except using hasattr()
        if td.a and not "/archive/" in td.a['href']:
            # drop the leading "/"
            nextpasteID = td.a['href'][1::]
            logging.info('Found ref to paste %s', nextpasteID)
            if not pastes.find_one({'id': nextpasteID}):
                logging.info('Retrieving paste %s', nextpasteID)
                paste = getpaste(nextpasteID)
                if paste:
                    logging.info('Inserting paste %s', nextpasteID)
                    pastes.insert(paste)
                else:
                    logging.info('Could not retrieve paste %s', nextpasteID)
                sleep(1)
            else:
                logging.info('Already have paste %s', nextpasteID)

    
    sleep(60)
