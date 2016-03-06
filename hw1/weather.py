#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import argparse
import requests
import json

parser = argparse.ArgumentParser()
parser.add_argument("-l", default="hsinchu" ,type=str ,help="locations")
parser.add_argument("-u", default="c" ,type=str , choices=['c','f'] ,help="unit")
parser.add_argument("-a", action='store_true' , help="equal to -c -d 5")
parser.add_argument("-c", action='store_true' , help="current condition")
parser.add_argument("-d", type=int , choices=[1,2,3,4,5] , help="forecasr")
parser.add_argument("-s", action='store_true' , help="sunset/sunrise")
args = parser.parse_args()

url = 'https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22'+args.l+'%22)%20and%20u=%27'+args.u+'%27&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys'
content = json.loads(requests.get(url).text)['query']['results']['channel']

if args.a:
    args.c = True
    args.d = 5

if args.c:
    print content['location']['city'] , ", " , content['item']['condition']['temp'],content['units']['temperature']

if args.d>=0:
    content = content['item']['forecast']
    for i in range(args.d):
        print content[i]['date'], content[i]['day'], content[i]['low'], "~", content[i]['high'],args.u.upper(), content[i]['text']

if args.s:
    print 'sunrise:',content['astronomy']['sunrise'],', sunset:',content['astronomy']['sunset']
