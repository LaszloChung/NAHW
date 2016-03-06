#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import urllib
import sys
from BeautifulSoup import BeautifulSoup
import requests
import json
import argparse
def html_unescape(s):
    htmlCodes = (
        ("'", '&#39;'),
        ('"', '&quot;'),
        ('>', '&gt;'),
        ('<', '&lt;'),
        ('&', '&amp;')
    )
    for code in htmlCodes:
        s = s.replace(code[1], code[0])
    return s

#=== parser ===
parser = argparse.ArgumentParser()
parser.add_argument("-n", default=5 ,type=int , help="number of search result.Default is 5")
parser.add_argument("-p", default=1 ,type=int , help="page that you parse")
parser.add_argument("keyword")
args = parser.parse_args()
url = "https://www.youtube.com/results?page="+ str(args.p) +"&search_query="
run = args.n
i = 0
#==============

webcon = urllib.urlopen(url+args.keyword)
soup = BeautifulSoup(webcon)
for result in soup.findAll("div", {'class':'yt-lockup-content'}):
    i += 1
    uncodeurl = "https://youtube.com" + result.a['href']
    encodeurl = "https://developer.url.fit/api/shorten?long_url=" + urllib.quote_plus(uncodeurl)
    BeautifulSoup(requests.get(uncodeurl).text).findAll("span", {'class':'yt-uix-button-content'})[14].text
    print result.a.contents[0] + " (https://url.fit/"+ json.loads(requests.get(encodeurl).text)['url'] +")"
    print html_unescape(result.findAll('div')[2].text)
    print "Like: " + BeautifulSoup(requests.get(uncodeurl).text).findAll("span", {'class':'yt-uix-button-content'})[14].text ,
    print ", Dislike: " + BeautifulSoup(requests.get(uncodeurl).text).findAll("span", {'class':'yt-uix-button-content'})[17].text
    print ""
    if i >= run:
        break
