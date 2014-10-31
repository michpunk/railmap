#!/bin/python

import argparse
import datetime
import urllib
import urllib2
import cookielib
import time
import re

def main():
  parser = argparse.ArgumentParser(description='Fetch journeys from ORIG to DEST at given DATE and TIME')
  parser.add_argument('orig', metavar='ORIG',
    help='station of departure')
  parser.add_argument('dest', metavar='DEST',
    help='station of origin')
  parser.add_argument('date', metavar='DATE',
    help='date of journey, e.g. 2010/12/01')
  parser.add_argument('time', metavar='TIME',
      help='time of journey, e.g. 18:00')
  args = parser.parse_args()
  orig = args.orig
  dest = args.dest
  time = args.time
  date = datetime.datetime.strptime(args.date, "%Y/%m/%d").date()

  ## TODO Convert time and date
  fetch (orig, dest, date, time)

def fetch(orig, dest, date, t):

  url = build_swt_url(orig, dest, date, t)

  cj = cookielib.CookieJar()
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
  response = opener.open('http://www.eastcoast.co.uk/')
  for cookie in cj:
    print cookie

  response = opener.open(url)
  for cookie in cj:
    print cookie
  page = response.read()
  ssid = get_session_id(page)
  enqId = get_enq_id(page)
  print enqId

  check_url = build_check_url(ssid)

  response = opener.open(check_url)
#  print response.read()
# Stub, but does not work anyway yet :) It looks like we need more
# params, for example enquiryId.
#  time.sleep(2)
#  response = opener.open(check_url)
#  print response.read()

def get_session_id(response):
  pat = re.compile('mixingDeck\.sessionId = \'\w*\'')
  tmpstr = pat.search(response)
  if tmpstr:
    return tmpstr.group()[24:-1]
  else:
    print "Error! No session ID found"

def get_enq_id(response):
  #TODO: this does not work at the moment. Find why :)
  pat = re.compile('mixingDeck\.enquiryIds = \[ \d*\]')
  tmpstr = pat.search(response)
  if tmpstr:
    return tmpstr.group()[26:-1]
  else:
    print "Error! No enq ID found"

def build_check_url(ssid):
  check_url = "http://tickets.eastcoast.co.uk/ec/en/JourneyPlanning/CheckForFTAEnquiryCompletion.aspx"
  data = {}
  data['cnt'] = '1'
  data['resend'] = 'Y'
  data['sess'] = ssid
  url_values = urllib.urlencode(data)
  check_url = check_url + '?' + url_values
  return check_url

def build_swt_url(orig, dest, date, time):
  base_url = "https://tickets.eastcoast.co.uk/ec/en/Landing/tis.aspx"
  data = {}
  data['od'] = orig
  data['dd'] = dest
  data['outd'] = str(date.day)
  data['outm'] = str(date.month)
  data['outda'] = 'y'
  data['outh'] = '05'
  data['outmi'] = '00'
  url_values = urllib.urlencode(data)
  full_url = base_url + '?' + url_values
  return full_url

if __name__ == '__main__':
      main()
